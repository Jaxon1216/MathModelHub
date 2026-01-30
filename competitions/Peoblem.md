# 2026年MCM问题C：星光下的数据
## 节目背景
《与星共舞》（Dancing with the Stars，简称DWTS）是国际电视节目特许经营权的美国版本，改编自英国节目《舞动奇迹》（原名《来吧，跳舞》）。该节目的版本已在阿尔巴尼亚、阿根廷、澳大利亚、中国、法国、印度等多个国家推出。本问题聚焦的美国版本已完成34季。

 celebrities 与专业舞者搭档，每周进行舞蹈表演。专业评委团为每对搭档的舞蹈打分，观众则通过电话或网络投票支持当周最喜爱的搭档。观众可投票一次或多次，但需不超过每周公布的投票上限。此外，观众投票是为支持希望留存的明星，而非投票淘汰明星。评委打分与观众投票将结合，以决定当周需淘汰的搭档（综合得分最低者）。每季有3对（部分季数更多）搭档晋级决赛，决赛周将结合观众与评委的综合得分，对晋级者进行1至3名（或4至5名）的排名。

评委打分与观众投票的结合方式多种多样。在美国版节目的前两季，采用基于排名的结合方式。由于第2季出现争议（名人参赛者杰瑞·赖斯尽管评委得分极低，仍晋级决赛），节目对规则进行了修改，改用百分比而非排名来结合打分与投票。附录中提供了这两种方式的示例。

第27季再次出现“争议”——名人参赛者鲍比·伯恩斯尽管评委得分持续偏低，却最终夺冠。对此，从第28季开始，节目对淘汰流程进行了微调：先通过结合评委得分与观众投票确定排名最后两位的参赛者，再由评委在直播节目中投票决定淘汰其中一方。大约在同一季，制作方还恢复了前两季采用的“基于排名”的结合方式（评委得分与观众投票的结合）。这一规则变更的确切季数尚未明确，但可合理推测为第28季。

评委打分旨在反映舞者的技术水平，但舞蹈优劣的评判存在一定主观性。观众投票的主观性可能更强，不仅受舞蹈质量影响，还与名人的人气和个人魅力相关。实际上，节目制作方在某种程度上可能更倾向于出现观点与投票冲突的情况，因为此类事件能提升观众的关注度和兴奋度。

## 数据说明
提供包含评委打分和参赛者信息的数据（如下文所述）。你可自行决定是否纳入额外信息或其他数据，但必须完整记录信息来源。利用该数据完成以下任务：

### 任务一：粉丝投票估算模型
构建数学模型（或多个模型），估算每位参赛者在其参赛的每周所获得的观众投票数（观众投票数属于未公开的保密信息）。
- 你的模型估算出的观众投票数是否能得出与每周淘汰结果一致的结论？请提供一致性的衡量指标。
- 你得出的观众投票总数估算结果的确定性如何？这种确定性对每位参赛者/每一周是否始终相同？请为估算结果的确定性提供衡量指标。

### 任务二：投票结合方式分析
利用估算的观众投票数及其他数据完成以下分析：
- 对比节目采用的两种投票结合方式（即基于排名和基于百分比）在各季中的结果（需将两种方式应用于每一季）。若结果存在差异，其中一种方式是否比另一种更偏向观众投票？
- 针对存在“争议”（即评委与观众意见存在分歧）的特定名人参赛者，分析两种投票结合方式的应用效果。对于每位此类参赛者，选择不同的评委得分与观众投票结合方式是否会导致相同结果？若采用“由评委从排名最后两位的搭档中选择淘汰对象”这一额外规则，会对结果产生何种影响？你可考虑以下示例（也可自行识别其他案例）：
  - 第2季——杰瑞·赖斯：尽管有5周的评委得分最低，仍获得亚军。
  - 第4季——比利·雷·赛勒斯：尽管有6周的评委得分排名最后，仍获得第5名。
  - 第11季——布里斯托尔·佩林：12次获得最低评委得分，最终获得第3名。
  - 第27季——鲍比·伯恩斯：尽管评委得分持续偏低，仍夺得冠军。
- 基于你的分析，你推荐未来季数采用哪种结合方式？请说明原因。你是否建议纳入“由评委从排名最后两位的搭档中选择淘汰对象”这一额外规则？

### 任务三：影响因素分析
利用包含估算观众投票数的数据，构建模型分析专业舞者以及数据中可获取的名人参赛者特征（如年龄、行业等）所产生的影响。这些因素对名人参赛者的比赛表现影响程度如何？它们对评委打分和观众投票的影响是否相同？

### 任务四：新投票系统设计
设计一套新的每周观众投票与评委打分结合体系，你认为该体系更“公平”（或在其他方面更优，例如能让节目对观众更具吸引力）。请说明该体系应被节目制作方采用的理由。

## 报告要求
提交一份不超过25页的报告，呈现你的研究结果，并附上1-2页的备忘录，总结核心结论，为《与星共舞》制作方提供关于评委打分与观众投票结合方式影响的建议，以及未来季数的应用推荐。

你的PDF解决方案（总页数不超过25页）应包含：
- 1页摘要页；
- 目录；
- 完整的解决方案；
- 1-2页备忘录；
- 参考文献列表；
- 人工智能使用报告（若使用，不计入25页限制）。

注：MCM提交的解决方案无特定最低页数要求。你可使用最多25页呈现所有解决方案内容及其他需补充的信息（如图表、计算过程、表格等）。部分解决方案也可被接受。允许谨慎使用ChatGPT等人工智能工具，但并非解决该问题的必要条件。若选择使用生成式人工智能，必须遵守COMAP的人工智能使用政策，并在PDF解决方案文件末尾添加额外的人工智能使用报告（不计入25页限制）。

## 数据文件说明
数据文件：2026_MCM_Problem_C_Data.csv——包含第1至34季的参赛者信息、比赛结果及每周评委打分。数据说明如表1所示。

表1：2026_MCM_Problem_C_Data.csv数据说明
| 变量 | 解释 | 示例 |
| ---- | ---- | ---- |
| celebrity_name | 名人参赛者（明星）姓名 | 杰瑞·赖斯、马克·库班等 |
| ballroom_partner | 专业舞者搭档姓名 | 谢丽尔·伯克、德里克·霍夫等 |
| celebrity_industry | 明星职业类别 | 运动员、模特等 |
| celebrity_homestate | 明星所在州（若来自美国） | 俄亥俄州、缅因州等 |
| celebrity_homecountry/region | 明星所在国家/地区 | 美国、英国等 |
| celebrity_age_during_season | 明星在该季的年龄 | 32、29等 |
| season | 节目季数 | 1、2、3……32 |
| results | 明星的赛季结果 | 冠军、第2周淘汰等 |
| placement | 赛季最终排名（1为最佳） | 1、2、3等 |
| weekX_judgeY_score | X周Y评委的打分 | 1、2、3等 |

### 数据备注
1. 每次舞蹈的评委打分范围为1（最低）至10（最高）：
   a. 部分周次的得分包含小数（如8.5），原因是该名人在当周表演了多个舞蹈，得分取各舞蹈的平均值；
   b. 部分周次会颁发加分（如舞蹈对决等），加分将平均分配至各评委/各舞蹈的得分中；
   c. 团队舞蹈得分将与每位团队成员的个人得分取平均值。
2. 评委按打分顺序排列；因此，“Y评委”在不同周次或不同季数中可能并非同一人。
3. 各季的参赛名人数量不同，节目播出的周数也不同。
4. 第15季是唯一一季由往届名人组成全明星阵容的季数。
5. 偶尔会出现某周无名人被淘汰，或某周淘汰多人的情况。
6. 数据集中的“N/A”值出现情况如下：
   a. 若某周无第4位评委，则第4位评委的得分为“N/A”（通常有3位评委）；
   b. 某季未播出的周次（例如，第1季仅播出6周，因此第7至11周的记录为“N/A”）。
7. 被淘汰的名人将记录为0分。例如，第1季中，首位被淘汰的名人是翠斯塔·萨特（在第2周节目结束时被淘汰），因此她在该季剩余周次（第3至6周）的得分为0。

## 附录：投票方式示例
### 1. 基于排名的结合方式（用于第1、2季及第28季至第34季）
第1、2季采用基于排名的方式结合评委打分与观众投票。例如，第1季第4周有4位剩余参赛者，雷切尔·亨特被淘汰，意味着她的综合排名最低。表2展示了该周的评委得分及排名，同时提供了一组可能的观众投票数据（仅为示例，旨在得出正确结果）。能产生相同结果的观众投票数据有多种可能，请勿将此示例数据视为实际值。由于雷切尔的评委排名为第2，要使她的综合排名最低，其观众投票排名需为第4，综合排名总分为6。

表2：基于排名的评委打分与观众投票结合示例（第1季第4周）
| 参赛者 | 评委总得分 | 评委排名 | 观众投票数* | 观众排名* | 综合排名总分 |
| ---- | ---- | ---- | ---- | ---- | ---- |
| 雷切尔·亨特 | 25 | 2 | 110万 | 4 | 6 |
| 乔伊·麦金泰尔 | 20 | 4 | 370万 | 1 | 5 |
| 约翰·奥赫利 | 21 | 3 | 320万 | 2 | 5 |
| 凯利·莫纳哥 | 26 | 1 | 200万 | 3 | 4 |

注：观众投票数/排名为未知数据，此处为假设值，旨在得出正确的最终排名。

### 2. 基于百分比的结合方式（用于第3季至第27季）
从第3季开始，节目改用百分比而非排名来结合得分与投票。以下以第5季第9周为例进行说明，该周詹妮·加斯被淘汰。同样，此处的观众投票数据为人工设定，旨在通过百分比计算得出正确结果。评委百分比的计算方式为：该参赛者的评委总得分除以所有4位参赛者的评委总得分之和。根据评委百分比，詹妮排名第3；但将人工设定的1000万观众投票所对应的百分比与评委百分比相加后，詹妮排名第4。

表3：基于百分比的评委打分与观众投票结合示例（第5季第9周）
| 参赛者 | 评委总得分 | 评委得分百分比 | 观众投票数* | 观众投票百分比* | 百分比总和 |
| ---- | ---- | ---- | ---- | ---- | ---- |
| 詹妮·加斯 | 29 | 29/117 = 24.8% | 110万 | 1.1/10 = 11% | 35.8% |
| 玛丽·奥斯蒙德 | 28 | 28/117 = 23.9% | 370万 | 3.7/10 = 37% | 60.9% |
| 梅尔·B | 30 | 30/117 = 25.6% | 320万 | 3.2/10 = 32% | 57.8% |
| 赫利奥·卡斯特罗内维斯 | 30 | 30/117 = 25.6% | 200万 | 2/10 = 20% | 45.6% |
| 总计 | 117 | - | 1000万 | - | - |

注：观众投票数为未知数据，此处为假设值，旨在得出正确的最终排名。
注：恢复基于排名的结合方式的确切年份尚未明确，合理推测为第28季。

---
# 2026 MCM
## Problem C: Data With The Stars
Dancing with the Stars (DWTS) is the American version of an international television franchise based on the British show “Strictly Come Dancing” (“Come Dancing” originally). Versions of the show have appeared in Albania, Argentina, Australia, China, France, India, and many other countries. The U.S. version, the focus of this problem, has completed 34 seasons.

Celebrities are partnered with professional dancers and then perform dances each week. A panel of expert judges scores each couple’s dance, and fans vote (by phone or online) for their favorite couple that week. Fans can vote once or multiple times up to a limit announced each week. Further, fans vote for the star they wish to keep, but cannot vote to eliminate a star. The judge and fan votes are combined in order to determine which couple to eliminate (the lowest combined score) that week. Three (in some seasons more) couples reach the finals and in the week of the finals the combined scores from fans and judges are used to rank them from \(1^{st}\) to \(3^{rd}\) (or \(4^{th}\), \(5^{th}\)).

There are many possible methods of combining fan votes and judge scores. In the first two seasons of the U.S. show, the combination was based on ranks. Season 2 concerns (due to celebrity contestant Jerry Rice who was a finalist despite very low judge scores) led to a modification to use percentages instead of ranks. Examples of these two approaches are provided in the Appendix.

In season 27, another “controversy” occurred when celebrity contestant Bobby Bones won despite consistently low judges scores. In response, starting in season 28 a slight modification to the elimination process was made. The bottom two contestants were identified using the combined judge scores and fan votes, and then during the live show the judges voted to select which of these two to eliminate. Around this same season, the producers also returned to using the method of ranks to combine judges scores with fan votes as in seasons one and two. The exact season this change occurred is not known, but it is reasonable to assume it was season 28.

Judge scores are meant to reflect which dancers are technically better, although there is some subjectivity in what makes a dance better. Fan votes are likely much more subjective, influenced by the quality of the dance, but also the popularity and charisma of the celebrity. Show producers might actually prefer, to some extent, conflicts in opinions and votes as such occurrences boost fan interest and excitement.

| ©2026 by COMAP | www.comap.org | www.mathmodels.org | info@comap.org |

Data with judges scores and contestant information is provided and described below. You may choose to include additional information or other data at your discretion, but you must completely document the sources. Use the data to:
1. Develop a mathematical model (or models) to produce estimated fan votes (which are unknown and a closely guarded secret) for each contestant for the weeks they competed.
   - Does your model correctly estimate fan votes that lead to results consistent with who was eliminated each week? Provide measures of the consistency.
   - How much certainty is there in the fan vote totals you produced, and is that certainty always the same for each contestant/week? Provide measures of your certainty for the estimates.
2. Use your fan vote estimates with the rest of the data to:
   - Compare and contrast the results produced by the two approaches used by the show to combine judge and fan votes (i.e. rank and percentage) across seasons (i.e. apply both approaches to each season). If differences in outcomes exist, does one method seem to favor fan votes more than the other?
   - Examine the two voting methods applied to specific celebrities where there was “controversy”, meaning differences between judges and fans. Would the choice of method to combine judge scores and fan votes have led to the same result for each of these contestants? How would including the additional approach of having judges choose which of the bottom two couples to eliminate each week impact the results? Some examples you might consider (there may also be others you identified):
     - Season 2 – Jerry Rice, runner up despite the lowest judges scores in 5 weeks.
     - Season 4 – Billy Ray Cyrus was \(5^{th}\) despite last place judge scores in 6 weeks.
     - Season 11 – Bristol Palin was \(3^{rd}\) with the lowest judge scores 12 times.
     - Season 27 – Bobby Bones won despite consistently low judges scores
   - Based on your analysis, which of the two methods would you recommend using for future seasons and why? Would you suggest including the additional approach of judges choosing from the bottom two couples?
3. Use the data including your fan vote estimates to develop a model that analyzes the impact of various pro dancers as well as characteristics for the celebrities available in the data (age, industry, etc). How much do such things impact how well a celebrity will do in the competition? Do they impact judges scores and fan votes in the same way?
4. Propose another system using fan votes and judge scores each week that you believe is more “fair” (or “better” in some other way such as making the show more exciting for the fans). Provide support for why your approach should be adopted by the show producers.

Produce a report of no more than 25 pages with your findings and include a one- to two-page memo summarizing your results with advice for producers of DWTS on the impact of how judge and fan votes are combined with recommendations for how to do so in future seasons.

| ©2026 by COMAP | www.comap.org | www.mathmodels.org | info@comap.org |

Your PDF solution of no more than 25 total pages should include:
- One-page Summary Sheet.
- Table of Contents.
- Your complete solution.
- One- to two-page memo.
- References list.
- AI Use Report (If used does not count toward the 25-page limit.)

Note: There is no specific required minimum page length for a complete MCM submission. You may use up to 25 total pages for all your solution work and any additional information you want to include (for example: drawings, diagrams, calculations, tables). Partial solutions are accepted. We permit the careful use of AI such as ChatGPT, although it is not necessary to create a solution to this problem. If you choose to utilize a generative AI, you must follow the COMAP AI use policy. This will result in an additional AI use report that you must add to the end of your PDF solution file and does not count toward the 25 total page limit for your solution.

Data File: 2026_MCM_Problem_C_Data.csv – contestant information, results, and judges scores by week for seasons 1 – 34. The data description is provided in Table 1.

## Table 1: Data Description for 2026_MCM_Problem_C_Data.csv
| Variables | Explanation | Example |
| --- | --- | --- |
| celebrity_name | Name of celebrity contestant (Star) | Jerry Rice, Mark Cuban, … |
| ballroom_partner | Name of professional dancer partner | Cheryl Burke, Derek Hough, … |
| celebrity_industry | Star profession category | Athlete, Model, … |
| celebrity_homestate | Star home state (if from U.S.) | Ohio, Maine, … |
| celebrity_homecountry/region | Star home country/region | United States, England, … |
| celebrity_age_during_season | Age of the star in the season | 32, 29, … |
| season | Season of the show | 1, 2, 3, …, 32 |
| results | Season results for the star | 1st Place, Eliminated Week 2, … |
| placement | Final place for the season (1 best) | 1, 2, 3, … |
| weekX_judgeY_score | Score from judge Y in week X | 1, 2, 3, … |

### Notes on the data:
1. Judges scores for each dance are from 1 (low) to 10 (high).
   a. In some weeks the score reported includes a decimal (e.g. 8.5) because each celebrity performed more than one dance and the scores from each are averaged.
   b. In some weeks, bonus points were awarded (dance offs etc); they are spread evenly across judge/dance scores.
   c. Team dance scores were averaged with scores for each individual team member.
2. Judges are listed in the order they scored dances; thus “Judge Y” may not be the same judge from week to week, or season to season.
3. The number of celebrities is not the same across the seasons, nor is the number of weeks the show ran.
4. Season 15 was the only season to feature an all-star cast of returning celebrities.
5. There are occasionally weeks when no celebrity was eliminated, and others where more than one was eliminated.
6. N/A values occur in the data set for
   a. the \(4^{th}\) judge score if there is no \(4^{th}\) judge for that week (usually there are 3) and
   b. in weeks that the show did not run in a season (for example, season 1 lasted 6 weeks so N/A values are recorded for weeks 7 thru 11).
7. A 0 score is recorded for celebrities who are eliminated. For example, in Season 1 the first celebrity eliminated was Trista Sutter at the end of the Week 2 show. She thus has scores of 0, 0 for the rest of the season (week 3 through week 6).

| ©2026 by COMAP | www.comap.org | www.mathmodels.org | info@comap.org |

## Appendix: Examples of Voting Schemes
### 1. COMBINED BY RANK (used in seasons 1, 2, and 28a - 34)
In seasons 1 and 2, judges and fan votes were combined by rank. For example, in season 1, week 4 there were four remaining contestants. Rachel Hunter was eliminated meaning she received the lowest combined rank. In Table 2, the judges scores and ranks are shown, and we created one possible set of fan votes that would produce the correct result. There are many possible values for fan votes that would also give the same results. You should not use these as actual values as this is just one example. Since Rachel was ranked \(2^{nd}\) by judges, in order to finish with the lowest combined score, she has the lowest fan vote (\(4^{th}\) place) for a total rank of 6.

## Table 2: Example of Combining Judge and Fan Votes by Rank (Season 1, Week 4)
| Contestant | Total Judges Score | Judges Score Rank | Fan Vote* | Fan Rank * | Sum of Ranks |
| --- | --- | --- | --- | --- | --- |
| Rachel Hunter | 25 | 2 | 1.1 million | 4 | 6 |
| Joey McIntyre | 20 | 4 | 3.7 million | 1 | 5 |
| John O’Hurley | 21 | 3 | 3.2 million | 2 | 5 |
| Kelly Monaco | 26 | 1 | 2 million | 3 | 4 |

* Fan vote/rank are unknown, hypothetical values chosen to produce the correct final ranks

### 2. COMBINED BY PERCENT (used for season 3 through 27a)
Starting in season 3, scores were combined using percents instead of ranks. An example is shown using week 9 of season 5. In that week, Jennie Garth was eliminated. Again, we artificially created fan votes that produce total percents to correctly lead to that result. The judges’ percent is computed by dividing the total judge score for the contestant by the sum of total judge scores for all 4 contestants. Based on the judges’ percent, Jennie was \(3^{rd}\). However, adding the percent of the 10 million artificially created fan votes we assigned to the judges’ percent, she was \(4^{th}\).

| ©2026 by COMAP | www.comap.org | www.mathmodels.org | info@comap.org |

## Table 3: Example of Combining Judge and Fan Votes by Percent (Season 5, Week 9)
| Contestant | Total Judges Score | Judges Score Percent | Fan Vote* | Fan Percent * | Sum of Percents |
| --- | --- | --- | --- | --- | --- |
| Jennie Garth | 29 | 29/117 = 24.8% | 1.1 million | 1.1/10 = 11% | 35.8 |
| Marie Osmond | 28 | 28/117 = 23.9% | 3.7 million | 3.7/10 = 37% | 60.9 |
| Mel B | 30 | 30/117 = 25.6% | 3.2 million | 3.2/10 = 32% | 57.8 |
| Helio Castroneves | 30 | 30/117 = 25.6% | 2 million | 2/10 = 20% | 45.6 |
| Total | 117 | | 10 million | | |

* Fan vote is unknown, values hypothetical to produce the correct final standings  
a The year of the return to the rank based method is not known for certain; season 28 is a reasonable assumption.

| ©2026 by COMAP | www.comap.org | www.mathmodels.org | info@comap.org |