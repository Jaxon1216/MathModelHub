"""
问题四：图片导出脚本
用于从建模分析中导出所有可视化图片为PDF格式

运行方式：
    python export_figures.py
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
import os
import warnings

warnings.filterwarnings('ignore')

# ============================================================
# 配置
# ============================================================

plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
sns.set_theme(style='whitegrid')

FIGSIZE_WIDE = (12, 6)
FIGSIZE_NORMAL = (10, 6)
COLORS = {
    'primary': '#4682B4',
    'secondary': '#FF7F50',
    'accent': '#228B22',
    'neutral': '#708090'
}
DIFFICULTY_COLORS = {'Easy': '#2ecc71', 'Medium': '#f39c12', 'Hard': '#e74c3c'}

FIGURE_DIR = os.path.dirname(os.path.abspath(__file__)) + '/figures'
os.makedirs(FIGURE_DIR, exist_ok=True)

def save_fig(fig, filename):
    """保存图片为PDF格式"""
    filepath = os.path.join(FIGURE_DIR, filename)
    fig.savefig(filepath, bbox_inches='tight', facecolor='white')
    print(f"✅ 已保存: {filepath}")
    plt.close(fig)

# ============================================================
# 数据加载
# ============================================================

print("="*60)
print("问题四：图片导出脚本")
print("="*60)

df = pd.read_csv('../数据预处理/data_processed.csv')
df['date'] = pd.to_datetime(df['date'])

print(f"📊 数据加载完成: {len(df)} 条记录")

target = 'difficulty'
feature_cols = [
    'num_vowels', 'vowel_ratio', 'num_unique_letters', 'num_repeated_letters',
    'has_repeated', 'avg_letter_freq', 'min_letter_freq', 'max_letter_freq',
    'first_letter_freq', 'last_letter_freq'
]

# ============================================================
# 图1: 难度分布
# ============================================================

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

difficulty_counts = df['difficulty'].value_counts()
colors = [DIFFICULTY_COLORS[d] for d in difficulty_counts.index]
axes[0].bar(difficulty_counts.index, difficulty_counts.values, color=colors, 
            edgecolor='black', alpha=0.8)
axes[0].set_xlabel('Difficulty Level', fontsize=12)
axes[0].set_ylabel('Count', fontsize=12)
for i, (d, c) in enumerate(zip(difficulty_counts.index, difficulty_counts.values)):
    axes[0].text(i, c + 2, f'{c}\n({c/len(df)*100:.1f}%)', ha='center', fontsize=10)

for difficulty in ['Easy', 'Medium', 'Hard']:
    subset = df[df['difficulty'] == difficulty]['avg_tries']
    axes[1].hist(subset, bins=20, alpha=0.6, label=difficulty, 
                 color=DIFFICULTY_COLORS[difficulty], edgecolor='black')
axes[1].axvline(x=4.0, color='black', linestyle='--', linewidth=2, label='Easy/Medium')
axes[1].axvline(x=4.5, color='black', linestyle=':', linewidth=2, label='Medium/Hard')
axes[1].set_xlabel('Average Tries', fontsize=12)
axes[1].set_ylabel('Frequency', fontsize=12)
axes[1].legend()

for difficulty in ['Easy', 'Medium', 'Hard']:
    subset = df[df['difficulty'] == difficulty]['fail_rate']
    axes[2].hist(subset, bins=20, alpha=0.6, label=difficulty,
                 color=DIFFICULTY_COLORS[difficulty], edgecolor='black')
axes[2].set_xlabel('Fail Rate (%)', fontsize=12)
axes[2].set_ylabel('Frequency', fontsize=12)
axes[2].legend()

plt.tight_layout()
save_fig(fig, 'fig1_difficulty_distribution.pdf')

# ============================================================
# 图2: 特征与难度关系
# ============================================================

key_features = ['num_vowels', 'num_repeated_letters', 'avg_letter_freq', 'min_letter_freq']

fig, axes = plt.subplots(2, 2, figsize=(12, 10))
axes = axes.flatten()

for i, feat in enumerate(key_features):
    ax = axes[i]
    data = [df[df['difficulty'] == d][feat] for d in ['Easy', 'Medium', 'Hard']]
    bp = ax.boxplot(data, labels=['Easy', 'Medium', 'Hard'], patch_artist=True)
    
    for patch, d in zip(bp['boxes'], ['Easy', 'Medium', 'Hard']):
        patch.set_facecolor(DIFFICULTY_COLORS[d])
        patch.set_alpha(0.7)
    
    ax.set_xlabel('Difficulty Level', fontsize=11)
    ax.set_ylabel(feat, fontsize=11)

plt.tight_layout()
save_fig(fig, 'fig2_feature_by_difficulty.pdf')

# ============================================================
# 模型训练
# ============================================================

X = df[feature_cols].values
y = df[target].values

le = LabelEncoder()
y_encoded = le.fit_transform(y)

X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 最佳模型
best_model = RandomForestClassifier(n_estimators=200, max_depth=10, 
                                    min_samples_split=5, random_state=42)
best_model.fit(X_train_scaled, y_train)

y_pred_best = best_model.predict(X_test_scaled)

# ============================================================
# 图3: 模型对比（简化版）
# ============================================================

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score, f1_score

models = {
    'Logistic\nRegression': LogisticRegression(max_iter=1000, random_state=42),
    'Random\nForest': RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42),
    'Gradient\nBoosting': GradientBoostingClassifier(n_estimators=100, max_depth=5, random_state=42),
    'SVM': SVC(kernel='rbf', probability=True, random_state=42)
}

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
results = []

for name, model in models.items():
    cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=cv, scoring='accuracy')
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)
    test_acc = accuracy_score(y_test, y_pred)
    
    results.append({
        'Model': name,
        'CV Accuracy': cv_scores.mean(),
        'CV Std': cv_scores.std(),
        'Test Accuracy': test_acc
    })

results_df = pd.DataFrame(results)

fig, ax = plt.subplots(figsize=FIGSIZE_NORMAL)

x = np.arange(len(results_df))
width = 0.35

bars1 = ax.bar(x - width/2, results_df['CV Accuracy'], width, label='CV Accuracy',
               color=COLORS['primary'], edgecolor='black', alpha=0.8,
               yerr=results_df['CV Std'], capsize=4)
bars2 = ax.bar(x + width/2, results_df['Test Accuracy'], width, label='Test Accuracy',
               color=COLORS['secondary'], edgecolor='black', alpha=0.8)

ax.set_xlabel('Model', fontsize=12)
ax.set_ylabel('Accuracy', fontsize=12)
ax.set_xticks(x)
ax.set_xticklabels(results_df['Model'])
ax.legend()
ax.set_ylim(0, 1)

for bar in bars2:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
            f'{bar.get_height():.3f}', ha='center', fontsize=9)

plt.tight_layout()
save_fig(fig, 'fig3_model_comparison.pdf')

# ============================================================
# 图4: 混淆矩阵
# ============================================================

cm = confusion_matrix(y_test, y_pred_best)

fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=le.classes_, yticklabels=le.classes_, ax=ax)
ax.set_xlabel('Predicted', fontsize=12)
ax.set_ylabel('Actual', fontsize=12)

plt.tight_layout()
save_fig(fig, 'fig4_confusion_matrix.pdf')

# ============================================================
# 图5: 特征重要性
# ============================================================

feature_importance = pd.DataFrame({
    'Feature': feature_cols,
    'Importance': best_model.feature_importances_
}).sort_values('Importance', ascending=False)

fig, ax = plt.subplots(figsize=FIGSIZE_NORMAL)

fi_sorted = feature_importance.sort_values('Importance', ascending=True)
bars = ax.barh(fi_sorted['Feature'], fi_sorted['Importance'], 
               color=COLORS['primary'], edgecolor='black', alpha=0.8)

ax.set_xlabel('Feature Importance', fontsize=12)
ax.set_ylabel('Feature', fontsize=12)

top3 = fi_sorted.tail(3)['Feature'].tolist()
for bar, feat in zip(bars, fi_sorted['Feature']):
    color = COLORS['accent'] if feat in top3 else 'black'
    ax.text(bar.get_width() + 0.005, bar.get_y() + bar.get_height()/2,
            f'{bar.get_width():.3f}', va='center', fontsize=9, color=color)

plt.tight_layout()
save_fig(fig, 'fig5_feature_importance.pdf')

# ============================================================
# EERIE预测
# ============================================================

letter_freq = {
    'E': 12.70, 'A': 8.17, 'R': 5.99, 'I': 6.97, 'O': 7.51, 'T': 9.06, 'N': 6.75,
    'S': 6.33, 'L': 4.03, 'C': 2.78, 'U': 2.76, 'D': 4.25, 'P': 1.93, 'M': 2.41,
    'H': 6.09, 'G': 2.02, 'B': 1.49, 'F': 2.23, 'Y': 1.97, 'W': 2.36, 'K': 0.77,
    'V': 0.98, 'X': 0.15, 'Z': 0.07, 'J': 0.15, 'Q': 0.10
}

def extract_word_features(word):
    word = word.upper()
    letters = list(word)
    unique_letters = set(letters)
    
    vowels = set('AEIOU')
    num_vowels = sum(1 for l in letters if l in vowels)
    vowel_ratio = num_vowels / len(letters)
    
    num_unique = len(unique_letters)
    num_repeated = len(letters) - num_unique
    has_repeated = 1 if num_repeated > 0 else 0
    
    freqs = [letter_freq.get(l, 0) for l in letters]
    
    return {
        'num_vowels': num_vowels, 'vowel_ratio': vowel_ratio,
        'num_unique_letters': num_unique, 'num_repeated_letters': num_repeated,
        'has_repeated': has_repeated, 'avg_letter_freq': np.mean(freqs),
        'min_letter_freq': np.min(freqs), 'max_letter_freq': np.max(freqs),
        'first_letter_freq': letter_freq.get(letters[0], 0),
        'last_letter_freq': letter_freq.get(letters[-1], 0)
    }

eerie_features = extract_word_features('EERIE')
eerie_X = np.array([[eerie_features[col] for col in feature_cols]])
eerie_X_scaled = scaler.transform(eerie_X)

eerie_pred = best_model.predict(eerie_X_scaled)[0]
eerie_proba = best_model.predict_proba(eerie_X_scaled)[0]
eerie_difficulty = le.inverse_transform([eerie_pred])[0]

# ============================================================
# 图6: EERIE特征对比
# ============================================================

fig, axes = plt.subplots(2, 2, figsize=(12, 10))
axes = axes.flatten()

for i, feat in enumerate(key_features):
    ax = axes[i]
    
    for difficulty in ['Easy', 'Medium', 'Hard']:
        subset = df[df['difficulty'] == difficulty][feat]
        ax.hist(subset, bins=15, alpha=0.5, label=difficulty, 
                color=DIFFICULTY_COLORS[difficulty], edgecolor='black')
    
    eerie_val = eerie_features[feat]
    ax.axvline(x=eerie_val, color='red', linestyle='--', linewidth=3, label='EERIE')
    
    ax.set_xlabel(feat, fontsize=11)
    ax.set_ylabel('Frequency', fontsize=11)
    ax.legend(fontsize=9)

plt.tight_layout()
save_fig(fig, 'fig6_eerie_comparison.pdf')

# ============================================================
# 图7: EERIE预测概率
# ============================================================

fig, ax = plt.subplots(figsize=(8, 6))

colors = [DIFFICULTY_COLORS[cls] for cls in le.classes_]
bars = ax.bar(le.classes_, eerie_proba * 100, color=colors, edgecolor='black', alpha=0.8)

ax.set_xlabel('Difficulty Level', fontsize=12)
ax.set_ylabel('Probability (%)', fontsize=12)
ax.set_ylim(0, 100)

for bar, prob in zip(bars, eerie_proba):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
            f'{prob*100:.1f}%', ha='center', fontsize=12, fontweight='bold')

pred_idx = list(le.classes_).index(eerie_difficulty)
bars[pred_idx].set_edgecolor('red')
bars[pred_idx].set_linewidth(3)

plt.tight_layout()
save_fig(fig, 'fig7_eerie_probability.pdf')

# ============================================================
# 完成
# ============================================================

print("\n" + "="*60)
print("🎉 所有图片导出完成！")
print("="*60)
print(f"\n图片保存在: {FIGURE_DIR}")
for f in sorted(os.listdir(FIGURE_DIR)):
    if f.endswith('.pdf'):
        print(f"  - {f}")
