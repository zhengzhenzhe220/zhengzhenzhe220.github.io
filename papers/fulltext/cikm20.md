---
source: cikm20.pdf
pages: 9
converter: pymupdf4llm
converted_at: 2026-08-30T22:06:14+08:00
---

# **A Deep Prediction Network for Understanding Advertiser Intent and Satisfaction** 

Liyi Guo<sup>1</sup> , Rui Lu<sup>2</sup> , Haoqi Zhang<sup>1</sup> , Junqi Jin<sup>2</sup> , Zhenzhe Zheng*<sup>1</sup> , Fan Wu<sup>1</sup> , Jin Li<sup>2</sup> , Haiyang Xu<sup>2</sup> Han Li<sup>2</sup> , Wenkai Lu<sup>3</sup> , Jian Xu<sup>2</sup> , Kun Gai<sup>2</sup> 

1Shanghai Jiao Tong University, 2Alibaba Group, 3Tsinghua University {liyiguo1995, zhanghaoqi39, zhengzhenzhe}@sjtu.edu.cn, fwu@cs.sjtu.edu.cn {dashi.lr, junqi.jjq, echo.lj, shenzhou.xhy, lihan.lh, xiyu.xj}@alibaba-inc.com lwkmf@mail.tsinghua.edu.cn, jingshi.gk@taobao.com 

## **Abstract** 

For e-commerce platforms such as Taobao and Amazon, advertisers play an important role in the entire digital ecosystem: their behaviors explicitly influence users’ browsing and shopping experience; more importantly, advertiser’s expenditure on advertising constitutes a primary source of platform revenue. Therefore, providing better services for advertisers is essential for the long-term prosperity for e-commerce platforms. To achieve this goal, the ad platform needs to have an in-depth understanding of advertisers in terms of both their marketing intents and satisfaction over the advertising performance, based on which further optimization could be carried out to service the advertisers in the correct direction. In this paper, we propose a novel Deep Satisfaction Prediction Network (DSPN), which models advertiser intent and satisfaction simultaneously. It employs a two-stage network structure where advertiser intent vector and satisfaction are jointly learned by considering the features of advertiser’s action information and advertising performance indicators. Experiments on an Alibaba advertisement dataset and online evaluations show that our proposed DSPN outperforms state-of-the-art baselines and has stable performance in terms of AUC in the online environment. Further analyses show that DSPN not only predicts advertisers’ satisfaction accurately but also learns an explainable advertiser intent, revealing the opportunities to optimize the advertising performance further. 

## **CCS Concepts** 

• **Information systems** → **Online advertising** ; • **Applied computing** → **Electronic commerce** . 

This work was supported in part by National Key R&D Program of China No. 2019YFB2102200, in part by Alibaba Group through Alibaba Innovation Research Program, in part by China NSF grant No. 61902248, 61972252, 61972254, 61672348, and 61672353, in part by Joint Scientific Research Foundation of the State Education Ministry No. 6141A02033702, in part by the Open Project Program of the State Key Laboratory of Mathematical Engineering and Advanced Computing No. 2018A09. The opinions, findings, conclusions, and recommendations expressed in this paper are those of the authors and do not necessarily reflect the views of the funding agencies or the government. 

*Z. Zheng is the corresponding author. 

Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the full citation on the first page. Copyrights for components of this work owned by others than ACM must be honored. Abstracting with credit is permitted. To copy otherwise, or republish, to post on servers or to redistribute to lists, requires prior specific permission and/or a fee. Request permissions from permissions@acm.org. _CIKM ’20, October 19–23, 2020, Virtual Event, Ireland_ © 2020 Association for Computing Machinery. ACM ISBN 978-1-4503-6859-9/20/10...$15.00 https://doi.org/10.1145/3340531.3412681 


![](assets/cikm20/cikm20.pdf-0001-11.png)


<!-- Start of picture text -->
Advertiser Ad Platform<br>Tag 1: 12$<br>Initialize an ad unit Ad position 1: 1.3 …<br>Ad auctions;<br>PV: 5000 Generate report<br>ROI: 0.1<br>… PV:5000<br>ROI:0.1<br>…<br>Adjust the ad unit based  Tag 1: 12$ → 14$<br>on the report Add Tag 3: 10$<br>Ad position 1: 1.3 → 1.2<br>…<br>Ad auctions;<br>PV: 8000 Update report<br>ROI: 0.3<br>…<br>…<br><!-- End of picture text -->

**Figure 1: An representative interaction process between an advertiser and the ad platform.** 

## **Keywords** 

E-commerce; Display Advertisement; Advertiser Intent Identification; Advertiser Satisfaction Prediction 

### **ACM Reference Format:** 

Liyi Guo, Rui Lu, Haoqi Zhang, Junqi Jin, Zhenzhe Zheng, Fan Wu, Jin Li, Haiyang Xu, Han Li, Wenkai Lu, Jian Xu, and Kun Gai. 2020. A Deep Prediction Network for Understanding Advertiser Intent and Satisfaction. In _Proceedings of the 29th ACM International Conference on Information and Knowledge Management (CIKM ’20), October 19âĂŞ23, 2020, Virtual Event, Ireland_ . ACM, New York, NY, USA, 8 pages. https://doi.org/10.1145/3340531.3412681 

## **1 Introduction** 

As online-shopping growing rapidly in popularity, e-commerce platforms such as Taobao and Amazon have become a primary place for users to search and purchase products [7, 8, 10]. With a huge number of potential users in online platforms, an increasingly large number of sellers rely on e-commerce platforms for advertising their products. Although advertising expenses constitute a major revenue income of e-commerce platforms, little attention has been given to investigate advertiser’s behavior, intent or satisfaction either from academia or industry community. Previous studies mainly focused on modeling and understanding the behaviors of users, such as widely-studied Click-Through Rate (CTR) prediction [4, 6, 9, 11, 30, 31] and user intent or satisfaction estimation in diverse contexts [3, 12, 17, 18, 25, 27]. As an ad platform 

can be modeled as a two-sided market between users and advertisers [8], ignoring the actions and feedback from advertisers would significantly reduce the efficiency of user-advertiser matching, and deteriorate the performance of ad systems in the long term. From a recently launched survey for advertisers in Taobao displaying ad platform, we observe that around half of the new advertisers would leave the ad platform after ten days, due to their marketing goals are not well satisfied. Therefore, in this work, we initialize a new research direction: focusing on advertiser intent understanding and advertiser satisfaction prediction, which would be leveraged to further improve the performance of ad systems. 

Advertisers achieve their ad marketing goals through taking different actions for ad campaigns, resulting in frequent and rich interactions with the ad platforms. We illustrate one representative interaction process between an advertiser and the ad platform in Figure 1. The advertisers launch an ad campaign for a specific product by initializing an _ad unit_ : adding demographic tags of targeting users and setting basic bid prices. The ad unit participates in a series of ad auctions over a period of time, and the statistical indicators about the ad performance, such as CTR, CVR (Conversion Rate), ROI (Return of Investment), and etc, are recorded in a report. After observing the performance report, the advertiser would take several adjusting actions, such as adding/deleting some tags or modifying bid prices, to further improve the ad performance under the guideline of her marketing goal. The ad auction mechanisms would react to the adjustment of advertiser and generate new ad performance. We observe that if an advertiser is satisfied with the updated ad performance, in most cases she would like to continue to invest in advertising; otherwise, she would eventually close the ad campaign and leave the platform. Thus, the long-term revenue of ad platforms largely depends on whether the advertisers are satisfied with the performance of their ad campaigns. It is highly necessary to provide algorithms for the ad platforms to predict advertiser’s satisfaction. 

During the advertising campaign, heterogeneous advertisers would have quite different preferences over the performance indicators, demonstrating various marketing intents. Although our case study is in a display advertising system with cost per click (CPC), advertisers still have different marketing intents beyond Click numbers. For example, for new launched products, advertisers tend to reach users as many as possible in a given time period, in which PV (Page View) and Click number often act as the key factors; for the advertisers with the goal of maximizing transaction revenue, they would pay more attention to indicators of Paynum (Pay Number) and Payamt (Pay Amount). Figure 2 illustrates the examples of these two advertisers realizing their different intents through a series of actions. The first advertiser would like to maximize user impressions, while the second advertiser attempts to maximize revenue. To provide better personalized ad services and optimize ad system performance in correct directions, the ad platform needs to have a deep understanding of the marketing intents of advertisers. 

In this paper, we propose a novel advertiser-side Deep Satisfaction Prediction Network (DSPN), which jointly models the advertiser intent and predicts advertiser satisfaction. Specifically, DSPN is a supervised learning framework that employs a two-stage hierarchical structure: through transformation of features, attention mechanism and recurrent neural networks, the first stage leverages 


![](assets/cikm20/cikm20.pdf-0002-04.png)


<!-- Start of picture text -->
Smoothly increase bid from 30 to 90.  Smoothly increase bid from 150 to 300.<br>Raise bid<br>to 300.<br>Raise bid<br>to 800.<br>(a) Maximizing Impression. (b) Maximizing Revenue.<br>Figure 2: Advertisers realize their various intents through<br>increasing bid prices. To understand advertisers, we should<br>get more details to model and identify advertisers’ intents.<br><!-- End of picture text -->

both advertiser’s action information and various ad performance indicators to learn the potential intent, which is further fed into the second stage; the second stage models the relation between advertiser intent vector and satisfaction explicitly in a principled way. Based on the above architecture, DSPN automatically learns the connections among raw data, advertiser intent and metrics related to advertiser satisfaction in e-commerce. Our contributions of this work can be summarized as follows: 

(1) To the best of our knowledge, we are the first to consider advertiser-side intent identification and satisfaction prediction. We formally define advertiser intent as a multi-dimension weight vector over ad performance indicators, which can be derived from a mathematical optimization problem. We evaluate the advertiser’s satisfaction by a new metric based on the change of investment on ad campaigns. 

(2) We point out the challenges in directly applying user-sided models to the advertiser-sided problems since they did not model the intent in a unified continuous space. Thus, we propose a Deep Satisfaction Prediction Network (DSPN) which jointly model advertiser intent and satisfaction. By employing action fusion layer and recurrent network structures, DSPN effectively extracts information critical for understanding advertiser intent and satisfaction, from diverse data features underlying the interaction between advertisers and the ad platform. 

(3) We conduct extensive experiments on an Alibaba advertisement dataset. Results verify the effectiveness of DSPN both in satisfaction prediction and intent vector generation. The generated intent vector not only exhibits nice interpretation for advertiser’s behavior but also reveals the potential optimization objectives to further improve the advertiser satisfaction and ad system performance. Moreover, DSPN has now been deployed in Alibaba online advertiser churn prediction system and serves daily business requirements. 

## **2 Related Work** 

## **2.1 User Intent Modeling and Satisfaction Prediction** 

In traditional information retrieval literature, there are extensive existing work in predicting user satisfaction with a searching query under different user intents [3, 17, 26, 27]. In [26], the authors considered the keywords submitted in an ad auction as a direct expression of intent and use them to determine the relevance of the ad and user query. Recently, researchers initialized the direction 

of user intents modeling and user satisfaction prediction in recommendation systems [12, 18, 23, 25]. In [18], the authors identified different kinds of user intents in music recommendation system through interviews, surveys and quantitative approaches, and proposed a multi-level hierarchical model to predict user satisfaction based on their intents. In [25], the authors classified user intents in product searching into three categories, including target product searching, decision making and new product exploration. They observed that different intents usually imply different interaction patterns, which can be further used to predict user satisfaction. 

Advertiser intent modeling is different from these existing works in two main aspects. First, advertiser intent is more difficult to model than user intent. User intents in searching, recommendation system, and e-commerce platform are relatively explicit, accompanied with different behavior patterns, and can be identified into coarse discrete categories through surveys or interviews. According to our preliminary investigation, most of the advertisers’ intents are a mixture of different optimization objectives, including PV, CTR, CVR, etc. Thus, instead of classifying advertiser intents into pre-defined discrete categories, we need to quantify advertiser intents in a unified continuous space. Furthermore, advertisers do not have appropriate channels to explicitly express their preferences over different performance indicators in most ad platforms. Second, advertiser’s action is more complicated and dynamic than user behavior, the method to identify user intents is usually based on finegrained interaction signals, such as mouse clicks and dwell time, according to the observation that user’s behavior pattern is highly related to user’s instant intent. However, advertiser’s operations exhibit more complicated characteristics than user actions: different advertisers have different strategies for advertising, resulting in various action patterns; action patterns of the same advertiser could also change during an ad campaign due to the underlying evolving intents. Therefore, we may not only use fine-grained interaction signals to capture advertiser intent and satisfaction. 

## **2.2 User Click-through Rate Prediction** 

In e-commerce platforms, click-through rate (CTR) indicates the user’s interest and satisfaction over recommendation items. Recently, a number of works have been done in designing CTR prediction models via deep learning approaches [4, 6, 9, 19, 22, 29– 31]. Most of these models are based on the structure of embedding and multilayer perceptron [31]. To further improve the expression ability of the model, Wide & Deep [4] and DeepFM [11] used different modules to learn low-order and high-order features. PNN [19] proposed a product layer to capture interactive patterns between inter-field categories. DIN [31] introduced the attention mechanism in CTR prediction problem to capture user’s diverse interests. DIEN [30] further improved DIN by designing an additional network layer to capture the sequential interest evolving process. 

There are three main differences between advertiser satisfaction prediction and CTR prediction. First, we do not have a clear label of whether the advertiser is satisfied with the ad performance, while in CTR prediction, we can easily get the label by checking whether the user clicks the ads. Second, advertiser satisfaction is more complex than user click action. We not only need to consider advertisers’ satisfaction but also explore their hidden intent, which is the underlying factors to determine advertiser satisfaction, while most CTR 

prediction models do not explicitly learn the user intent. In this work, we also identify advertiser intent during satisfaction prediction. Finally, CTR prediction models aim at building a correlation between a user and an item. However, advertiser comes to the ad platform to improve ad performance or product sale volume instead of a specific item. Thus we should focus on building a correlation between an advertiser and her ad performance. 

## **3 Preliminaries** 

In this section, we first describe the interaction between advertisers and the displaying ad platform in Taobao. We then introduce the definitions of advertiser intent and satisfaction based on our observations from practical ad systems. 

In Figure 1, we show an example of the interaction between advertisers and the Taobao displaying ad platform, in which advertisers can start or close an ad campaign at an appropriate time and take various actions during the ad campaign to achieve their marketing goals. To initialize an ad campaign for an ad unit, the advertiser needs to choose a set of demographic tags and the corresponding basic bid prices to effectively and efficiently target the potential users. The advertiser would also select preferred ad positions (e.g., ad slots in “Home Page” or “After Shopping Page”) and a premium rate to improve the performance of ad exposure. The advertiser would like to declare a higher bid, i.e., _basic bid_ × _premium rate_ for the preferred ad positions. The advertisers participate in the ad auctions when targeting users visit the ad positions. If the ad unit wins the auction, the corresponding ad is shown to the users, and a certain price is charged to the advertiser once the user clicks the ad, following the cost per click (CPC) paradigm. Various auctions are conducted for the ad unit during the campaign, and the accumulated Key Performance Indicators (KPIs), such as CTR, Cost, ROI, and etc., are recorded in the report. After a certain period (e.g., one day or one week), the advertiser would check the KPIs report and conduct a series of actions to adjust the ad campaign when some performance indicators do not match her expectation. The potential operations of advertisers could be adding or deleting certain tags/positions or changing bid prices or premium rates. The ad unit with the adjusted features enters the ad auctions for competition and obtains new marketing performance. 

Our goal in this work is to formally define the metrics to measure the advertiser marketing intent and satisfaction, build a connection between them via extracting the useful information from the above interactions, and identify advertiser intent and predict advertiser satisfaction based on the proposed metrics and connection. 

## **3.1 Advertiser Intent Modeling** 

Advertisers use the Taobao ad platform with different marketing intents. However, existing work in the literature usually assumed the advertisers simply optimize a single objective, such as CTR or CVR, and the specific formulation of advertiser’s practical and various intents is not well established. Our main focus in this subsection is to evaluate advertiser intent based on a survey and an intuitive observation from a mathematical optimization model. 

To fully understand advertisers’ marketing goals, we conduct a survey with questions about the major reasons of using Taobao displaying ad platform and the preferred performance indicators. We collect feedback from 791 advertisers, and show the results in 

**Table 1: Summary of advertiser survey.** 

|MarketingIntents|Ratio|Indicators|Ratio|
|---|---|---|---|
|Target potential users actively|68%|ROI, CVR|86%|
|Lever non-advertisement traffic|52%|CTR, PPC|56%|
|Cost-effective advertising|46%|CART, CLT|55%|



Table 1. We note that the ratio of each column in Table 1 does not need to sum up to one, indicating the advertisers may have multiple intents and care for different performance indicators, such as ROI, CVR, CTR, CART ( _Add to Cart_ number) and CLT ( _Collection_ number), simultaneously. As a result, advertiser intent may not be simply characterized by a single indicator as in the existing work. Its formulation should reflect various concerns of the advertiser and contain the major indicators of the ad campaign. We introduce an advertiser-specific weight vector w = [ _w_ 1, _w_ 2, · · · , _wn_ ]<sup>⊤</sup> to define the advertiser’s intent by assigning each indicator an importance weight, which represents the advertiser’s preference over different indicators. One simple interpretation for the weight vector is that the advertiser may optimize her actions, such as adjusting bid or premium rate, through solving a multi-objective optimization problem. We can also derive the weight vector by solving the maximization problem for a specific indicator but with additional constraints for other indicators, which can be illustrated as follows: max _bid_<sup>_pv_</sup> (1) 


![](assets/cikm20/cikm20.pdf-0004-03.png)


where the performance indicators _pv_ , _click_ , _cost_ , _ppc_ are functions of _bid_ . By employing Lagrange multipliers, we can derive the following Lagrangian function for the above optimization problem: 


![](assets/cikm20/cikm20.pdf-0004-05.png)


where ˆw = [1, _w_ 1, − _w_ 2, − _w_ 3]<sup>⊤</sup> , _I_ = [ _pv_ , _click_ , _cost_ , _ppc_ ]<sup>⊤</sup> and _b_ = − _w_ 1 _α_ + _w_ 2 _β_ + _w_ 3 _γ_ . The Lagrange multipliers have a nice interpretation in economics [24]. We can regard the Lagrange multipliers as some kind of prices for violating the indicator constraint. Therefore, we consider the Lagrangian function L( _bid_ , ˆw) as the total benefit of declaring the _bid_ , and the vector [ ˆw<sup>⊤</sup> , _b_ ]<sup>⊤</sup> as the weight vector w of advertiser’s intent. However, there are several obstacles for optimizing (2) explicitly. Due to information asymmetry between the ad platform and the advertiser: the ad platform has no direct knowledge of the constraints in (1), e.g., the constraint parameters _α_ , _β_ , _γ_ . This may come from the scenario that the advertisers would not like to reveal this information due to privacy policy and business secret, or from the scenario that the advertisers may not have the feasible channels to express their optimization objectives in the current ad platform. 

To resolve the lack of information about optimization parameters, we have a critical observation from the interaction between the ad platform and advertisers. The intents motivate advertisers to take different actions after checking the performance report, and thus their intents can be estimated by their historical action traces, such as deleting or adding tag actions, and the performance report. From the previous advertiser survey, we also observe the marketing intent of advertisers is usually consistent during a certain period. Thus, we can use the advertiser’s historical information from a 

certain observation period to predict her current intent using our designed deep learning model in next section. 

## **3.2 Advertiser Satisfaction Modeling** 

It is quite challenging to determine whether the advertisers are satisfied with the performance of their ad units, compared with the scenario in the user’s side, where we have direct and clear signals, such as click or buying actions, to infer their satisfaction over recommendation items. One potential metric to measure the advertiser satisfaction level is the Lagrange function in (2), which is a weighted average of all advertising performance indicators. However, due to the above-mentioned information asymmetry, we are unable to calculate this metric exactly. 

From empirical observation, we find that various indicators are highly related to advertiser satisfaction, which could be exploited to define an appropriate metric to infer the level of advertiser satisfaction via indirect signals. Churn label is a classical satisfaction metric to measure a customer’s satisfaction over the subscribed services, e.g., various works [2, 16, 20, 28] define a churned customer in different contexts based on the following signals: (1) No placing an order over a year in ASOS platform [2], (2) No logging in over 30 consecutive days in TikTok platform [16], (3) No activity over a week in Snapchat [28]. Similarly, if an advertiser is unsatisfied with the performance of an ad unit, she would finally stop investing for the ad campaign. Thus we can adopt investment-related indicators to infer the advertiser’s satisfaction to some extent, such as take rate (the ratio of cost to GMV) or simply the cost level. From the above discussion, we regard an advertiser is unsatisfied with the performance of an ad unit during a period [ _l_ 0 − _l_ , _l_ 0) if the cost in period [ _l_ 0, _l_ 0 + _l_ ) is less than or equal to _ϵ_ , which is a small amount of money close to 0. Otherwise, the advertiser is satisfied with (or at least not so unsatisfied) with the ad unit. Usually, we do not set _ϵ_ equal to 0 because an advertiser may leave before her budget runs out. Due to the performance delay in the ad platform, we use the cost level in a later period to evaluate the satisfaction level in a previous period. With this definition, we can have a direct and easy-calculated signal to obtain the satisfaction label for the data. 

## **4 Deep Satisfaction Prediction Network** 

In this section, we propose a novel deep network architecture, Deep Satisfaction Prediction Network (DSPN), for the advertiser intent learning and satisfaction prediction. As shown in Figure 3, DSPN is a supervised learning framework with two stages: intent learning stage and satisfaction prediction stage. The learnable parameters are all deployed in the intent learning stage, which extracts information from the advertiser’s historical data to learn intent vector w, which is forwarded to the second stage. The satisfaction prediction stage combines the intent vector w and advertiser’s historical performance report to calculate whether an advertiser is satisfied over the performance of ad units. 

## **4.1 Input Features** 

We first investigate which types of features related to advertiser’s intent and satisfaction. As heterogeneous advertisers may have various intents and satisfaction levels for different ad units, the prediction model needs to involve the ID features of advertisers and ad units. It is obvious that the specific values of KPIs in the 

report are highly related to the advertiser’s satisfaction levels. Thus, we also need to consider the performance indicators during the training of prediction model. Advertisers’ behavior patterns have certain relation with their satisfaction over the ad performance. For example, when we count the number of actions of an advertiser for a specific ad unit during an observation period with length 10, we find that the average number of modification actions in positive label (satisfied) is 11.179, while the mean in negative label (unsatisfied) is 9.790, indicating that satisfied advertisers tend to achieve the desired ad performance through frequent adjustments of bid prices and premium rates. Moreover, for the number of “add tag” actions, the mean of positive label is 1.274, and negative label 1.267, which are close. However, for the number of “delete tag” actions, the mean of positive label is 0.178 more than that of negative label, which is 0.109. These findings indicate that satisfied advertiser tends to adjust her strategy by deleting demographic tags which she thinks not so important after some trials. Therefore, we also need to consider the actions of advertisers in the model. 

From the above discussion, the input of DSPN contain three types of features: ID features, performance indicators and action features, from an observation period. We further divide action features into ultimate actions and sequential actions. The ultimate actions represent the advertiser’s strategy at the end of the day, containing tags’ final bid prices and ad positions’ premium rates. The sequential actions represent the intermediate actions the advertiser has done during the day to achieve her marketing intents. The specific formats of the data sets are described in Section 5. 

## **4.2 Embedding Layer** 

We transform our sparse features into low-dimensional dense features through embedding. For categorical feature, e.g. ID features, we convert them into a dense real-valued embedding vector m. For features with both categorical and numerical information, we present them with e = _v_ ⊙ m, where the embedding vector m indicates categorical information, the value _v_ is the normalized value indicating numerical information, and ⊙ is the element-wise product operator. Furthermore, the value _v_ of performance indicator feature is the value of the corresponding KPI; the value _v_ of ultimate action feature is the value of bid price/premium rate at the end of the day; the value _v_ of sequential action feature is the value of bid price/premium rate after the action minus the value before the action. 

After the embedding layer, features of the same type like ID features are concatenated into a vector. Fully-connected layers are used for reshape the vector when necessary. For sequential action features, we further divide them into two groups: tag features and ad position features. Each of the group contains a sequence of action features within the day, and we connect the embedding vectors of these actions chronologically to form a list represented by _E_ = [e1, e2, ..., e _na_ ] ∈ R<sup>_ne_×</sup><sup>_na_</sup> , where e _i_ is the embedding vector of the _i_ -th sequential action with dimension _ne_ , and _na_ represents the number of actions in this group within a day. The embedding layer is trained at the same time with the model during the training process. We use sum/average pooling to transform multiple embedding vectors into a fixed-length vector when necessary. 

## **4.3 Intent Learning Stage** 

In the intent learning stage, we employ multilayer bidirectional RNNs on the top to learn the advertiser intent based on information from _l_ sequential days. We use a fusion layer to capture important pattern in sequential actions for each day in the bottom. 

**Action Fusion Layer.** Advertiser’s sequential actions such as _“add a tag with price x”_ or _“delete a tag”_ contain rich information of her strategies or preferences over various KPIs. We use a fusion layer to get a summary of advertiser’s sequential actions within each day. Different approaches like sum pooling, average pooling or attention mechanism [1] can be used in the fusion layer. Since advertisers may try different actions before they finally figure out the correct actions to do within a day, we suggest employ the attention mechanism to identify important actions within the action sequence, considering the advertiser’s current situation. In detail, the attention mechanism is formulated as: 


![](assets/cikm20/cikm20.pdf-0005-08.png)


where _V_ ∈ R<sup>_na_×</sup><sup>_ne_</sup> is the sequential action matrix of one day and _V_ = _E_<sup>⊤</sup> , values of _na_ and _ne_ represent the number of actions in each day and the embedding dimension, respectively. The matrix _Q_ ∈ R<sup>_na_×</sup><sup>_ne_</sup> is the summary of the advertiser’s ID features, daily performance report and daily ultimate action information on the same day, and is reshaped to the same size as _V_ . One can obtain _Q_ through MLP, RNN or other structures. With the attention mechanism, we can learn an advertiser-specific representation for the action pattern. Matrix _V_ is given to the next level together with other feature representations after pooling. 

**RNN Layer.** Recurrent neural network models sequential data explicitly [15] and gives us inspiration to exploit the advertiser intent based on her historical information. Imagine the procedure that an advertiser reviews her recent ad performance and actions, and adjust the actions to obtain updated ad performance if her marketing intent is not well fulfilled. Thus, there are some underlying relation between advertiser actions and advertiser intent. We employ RNN to investigate the dynamic representation of advertiser’s daily information related to advertiser intent. To balance efficiency and performance, we employ GRU [5] as GRU overcomes vanishing gradient problem and is faster than LSTM [13]. The formulations of GRU are listed as follows: 


![](assets/cikm20/cikm20.pdf-0005-11.png)



![](assets/cikm20/cikm20.pdf-0005-12.png)



![](assets/cikm20/cikm20.pdf-0005-13.png)


where _et_ is the representation of _t_ -th day’s report and action information from the previous level, _st_ is the _t_ -th hidden states, _σ_ is the sigmoid function and ⊙ is the element-wise product operator. Because advertisers may review the historical information back and forth, we would like the representation of each day to summarize not only the preceding days, but also the following days. Hence, we propose to use two layers of bidirectional recurrent network (Bi-GRU) [21]. For each Bi-GRU layer, the hidden state of the _t_ -th day can be represented by concatenating the hidden state in the forward GRU and the backward GRU as _ht_ = [<sup>−→</sup> _h t_ ,<sup>←−</sup> _h t_ ]. We obtain 


![](assets/cikm20/cikm20.pdf-0006-00.png)


<!-- Start of picture text -->
Intent Learning Stage Satisfaction Prediction Stage<br>Bi-GRU Bi-GRU Bi-GRU Bi-GRU Dot Sigmoid<br>Report<br>Bi-GRU Bi-GRU Bi-GRU Bi-GRU<br>SUM Pooling SUM Pooling SUM Pooling SUM Pooling w Report Dot Sigmoid Average Pooling Output<br>Action Fusion Layer Action Fusion Layer Action Fusion Layer Action Fusion Layer<br>… Dot Sigmoid<br>Report<br>Concat & Flatten Concat & Flatten Concat & Flatten Concat & Flatten<br>Embedded Ad ID Features<br>Embedded Daily Performance Report Features<br>Embedded Daily Ultimate Action Features<br>Embedded Daily Sequential Action Features<br>…<br><!-- End of picture text -->

**Figure 3: Deep Satisfaction Prediction Network. The left part is the intent generation stage, which computes the intent vector** w **, the right part is the satisfaction prediction stage, which predicts advertiser satisfaction based on ad unit’s performance report and advertiser’s intent vector.** 

the representation of w by adding the _l_ 0 − 1-th day’s hidden state in the second Bi-GRU layer as w =<sup>−→</sup> _h l_ 0−1 +<sup>←−</sup> _h l_ 0−1. 

## **4.4 Satisfaction Prediction Stage** 

In satisfaction prediction stage, we build a connection between advertiser intent vector and advertiser satisfaction level. According to Section 3.1, there exists a positive correlation between w<sup>⊤</sup> _Ii_ and advertiser satisfaction, where _Ii_ represents the performance report in day _i_ . Following this intuition, we assign the probability of the advertiser being satisfied with the ad performance during the period [ _l_ 0 − _l_ , _l_ 0) as: 


![](assets/cikm20/cikm20.pdf-0006-05.png)


where _σ_ is sigmoid function and w is the advertiser intent vector learned from the previous stage. The loss function of the prediction model is defined as follows: 


![](assets/cikm20/cikm20.pdf-0006-07.png)


where D is the training set with size _N_ , _x_ is the input of the model and _y_ is the label. 

## **5 Experiments** 

In this section, we evaluate DSPN in detail and summarize our experiments as follows: (1) We verify the effectiveness of DSPN in intent identification and satisfaction prediction, and discuss the impact of different data features through offline experiments. (2) Analyses of intent vector w show that w can fully capture the advertiser intent in practice. (3) Online evaluation shows that our model performs well for different advertiser satisfaction modeling tasks and has stable performance with around 0.9334 ± 0.0028 AUC counting in 30 consecutive days. 

## **5.1 Experiment Setup** 

The dataset we used is collected from Alibaba displaying ad system. There are about 1 million ad units from around 1.6 × 10<sup>5</sup> advertisers in our dataset, and each ad unit forms a unique sample. The ad units we selected are those with cost larger than 10 units in 

period [ _l_ 0 − _l_ , _l_ 0). We randomly divide the data set into a training set and a test set according to a 9 : 1 ratio. Each data sample contains an ad unit’s information from the observation period [ _l_ 0 − _l_ , _l_ 0) with length _l_ = 10, and the satisfaction label is marked for each data sample using the definition in Section 3.2 with the parameters _l_ = 10 and _ϵ_ = 10. We set these parameters based on our business experience and data analysis. Specifically, when _l_ is too small, it may not reflect real satisfaction phenomenon of users; when _l_ is too large, it would involve many already churned ad units during the observation period, or the downstream tasks would wait a long time (at least _l_ days later) to get the satisfaction predicted results. The parameter _ϵ_ is a small amount of money that can prevent noisy data introduced by ad performance delay, and enable the model to do early churn warning before budget runs out. The details of main features in the dataset are summarized as follows: 

**ID Features.** ID features contain basic profile and identity information about ad unit, product category and advertiser, and are used to provide personalized information in model training. 

**Report Features.** Report features refer to the performance indicators of an ad unit within each day from the observation period. There are 15 indicators of report features in total, including Cost, CTR, CVR, ROI, and etc. 

**Action Features.** Action features contain the ultimate action feature and sequential action feature of the advertiser within the observation period. The detailed data format for action features are described in Table 2. 

We train DSPN with batch-GD algorithm with batch size 32, using the Adam optimizer [14]. The dimension of the hidden state in the first Bi-GRU layer is 18, the dimension of the hidden state in the second Bi-GRU layer is 16, which is the same as the dimension of w. Different categorical features have different embedding dimensions in DSPN from 3 to 18, which are fine-tuned to achieve good results. The source code is available online<sup>1</sup> . 

## **5.2 Comparative Models** 

The problem of advertiser satisfaction prediction we discussed is new in both academia and industry communities, and to the 

1https://github.com/liyiguo95/DSPN 

best of our knowledge, there are not related models in the literature. Considering that the prediction models for user-side problems are widespread and mature, we carefully select some widely used prediction models in user click-through rate prediction, slightly revised them to adopt to the scenario of advertiser satisfaction, and regard them as our baselines. 

**Embedding & MLP Model:** The Embedding & MLP model is a basic model of most subsequently developed deep networks [4, 6, 11, 19, 31] for CTR modeling. It contains three parts: embedding layer, pooling and concat layer, multilayer perceptron. 

**Wide & Deep [4]:** Wide & Deep model has been proved to be effective in recommendation systems. It consists of two parts: (1) Wide model, which is a linear model handles the manually designed features. (2) Deep model, which employs the Embedding & MLP Model to learn nonlinear relations among features automatically. 

**PNN [19]:** PNN can be viewed as an improved version of the Embedding & MLP Model by explicitly introducing a product layer after embedding layer to capture high-order feature interactions. 

**DeepFM [11]:** DeepFM imposes factorization machines as the “wide” part and multilayer perceptron as the “deep” part. The two parts in DeepFM are trained together and share the input. 

**DIN [31]:** Based on the Embedding & MLP Model, DIN uses the attention mechanism to activate related user behaviors. In our experiments, we implements DIN to learn the inner relationship between the advertiser profiling and daily features. 

## **5.3 Experimental Results** 

**Comparative Results.** Since the above mentioned models have different structures, to tune each baseline model, we use sum pooling, average pooling, and concatenation to integrate different features according to the specific model structure. The metrics used are Area Under the Curve (AUC) and Accuracy (ACC). From Table 3, we observe that DSPN outperforms other models in the problem of advertiser satisfaction prediction, achieving AUC of 0.9437 and ACC of 0.8928. We verify the effectiveness of DSPN through ablation studies of model structure. As shown in Table 3. DSPN with multilayer bidirectional GRU layers is superior to DSPN without GRU and DSPN with multilayer GRU. This result demonstrates that DSPN with bidirectional GRU layers in the first stage is more effective to extract useful patterns from the historical information than other designs. For the attention mechanism in the action fusion layer, we also test sum pooling, average pooling as the alternative fusion layer, and the results are similar. To shed some light on the advantages of the attention mechanism in broad scenarios: (1) We delete other features and only use sequential actions to perform the control experiments. (2) We also deploy DSPN in a similar task related to advertiser’s satisfaction: predicting whether an ad unit’s cost will increase in the next week, which highly relies on sequential action information. Compared with other strategies in the fusion layer, attention mechanism achieves better performance in both tasks with AUC increasing more than 3.0% and 1.6% respectively. We conclude that attention mechanism makes DSPN more robust to the tasks with relation to sequential action information. 

**Impact of Data Features.** To better understand the roles that different data features play in advertiser satisfaction prediction, we conduct two types of tasks using DSPN. The first task is to predict the advertiser satisfaction without a selected data feature, while 

the second task only uses the selected data feature for prediction. We show the results in Table 4, and can see that each data feature has a positive contribution to the performance of DSPN. ID feature contributes the least since it only provides basic information of an entity. However, we still maintain ID features so that information can be shared among the same entity. For example, ad units belong to certain categories may have good sale in some special time or areas. Thus, these ad units can then share the performance indicators for satisfaction prediction. Both daily report feature and action feature play important roles in satisfaction prediction. This observation shows that the advertiser satisfaction mainly depends on daily ad performance, which proves the necessity of optimizing the ad results under the guideline of advertiser’s intent. 

## **5.4 Intent Results Analysis** 

In this subsection, we show the validity and the effectiveness of the weight vector w learned from the first stage in representing various advertiser intents. We also show the necessity of considering advertiser intents when predicting their satisfaction. 

**Effectiveness of weight vector** w **in profiling intents.** We perform a _K-Means_ clustering analysis on the weight vector w in the test set and investigate whether w can capture the advertisers’ various intents. We use _Euclidean distance_ as the cluster metric in _K-Means_ clustering and use _PCA_ to reduce the dimensions of w from 16 to 2, then we visualize the sample distribution of different clusters in Figure 4. We find the obtained cluster centers well match the typical advertisers in practical ad systems. 

**Cluster 1: Active ad units.** Advertisers in this cluster are high quality customers to the ad platform. Most of advertisers feel satisfied with the ad units in this cluster, because the ad units have a stable and good performance in overall indicators. 

**Cluster 2: Maximizing Impression.** Advertisers in this cluster care more about PV and Click number, and they also care about cost. This indicates that advertisers would like to maximize impression or Click number in a cost-effective way. 

**Cluster 3: Maximizing Revenue.** Advertisers in this cluster are insensitive to the cost, and consider more on ROI and CVR. These ad units usually target the loyal customers or members in the advertiser’s Taobao shop. 

**Cluster 4: Tail ad units.** Advertisers in this cluster usually do not spend too much money in total. Performance indicators like click and pay amount have a positive impact in their satisfaction, while cost has a negative impact in their satisfaction. 

**Importance of advertiser intent in satisfaction prediction.** We design three experiments to figure out how different intents can significantly influence the performance of advertiser satisfaction, and show the results in Table 5. The first column in Table 5 shows the accuracy of predicting each advertiser’s satisfaction label with her report data _I_ and w from the center of the cluster she belongs to. The results show that these cluster centers can well predict the satisfaction of advertisers belonging to the same cluster, i.e., the advertisers having similar marketing intents. In the second experiment, we use each cluster center to predict the satisfaction label of advertisers in other clusters. The results in the second column of Table 5 show that the prediction accuracy is far worse than that in the same cluster as we mentioned above, indicating advertiser intents are different among clusters. In the third experiment, we 

**Table 2: Action features of Alibaba dataset.** 

|Feature Type|Target Type|Data Format|Data Explanation|
|---|---|---|---|
|Ultimate Action|Tag<br>|(_taд_type_,_bid_price_)<br>|bid for tags end of the day<br>|
||Ad Position|(_position_type_,_premium_rate_)<br>|premium rate for ad positions end of the day<br>|
|||(_taд_type_,_price_,_time_)<br>|add a tag with a bid<br>|
||Tag|(_taд_type_,_old_price_,_new_price_,_time_)<br>|change bid for a tag<br>|
|Seuential Action||(_taд_type_,_current_price_,_time_)<br>|delete a chosen tag<br>|
|q||(_position_type_,_rate_,_time_)|add an ad position with a premium rate|
||Ad Position|(_position_type_,_old_rate_,_new_rate_,_time_)<br>|change premium rate for an ad position<br>|
|||(_position_type_,_current_rate_,_time_)|delete a chosen ad position|



**Table 3: Comparisons of different models.** 

|Model|AUC|ACC|
|---|---|---|
|MLP|0.8501|0.7975|
|Wide & Deep|0.8507|0.7968|
|<br>PNN|0.8519|0.7989|
|DeepFM|0.8538|0.8005|
|DIN|0.8562|0.7951|
|DSPN without GRU|0.9001|0.8414|
|DSPN with multilayer GRU|0.9415|0.8917|
|<br>DSPN with multilayer bidirectional GRU|**0.9437**|**0.8928**|



**Table 4: Impact of different features. Results of tasks without a selected feature are on the left, and results of tasks only with the selected feature are on the right.** 

|Task|AUC|ACC|Task|AUC|ACC|
|---|---|---|---|---|---|
|w/o ID<br>|0.9428|0.8924|w ID<br>|0.8241|0.7669|
|w/o Action<br>|0.9410|0.8903|w Action<br>|0.9300|0.8853|
|w/o Report|**0.9336**|**0.8860**|w Report|**0.9368**|**0.8890**|



**Table 5: Results of intent effectiveness.** 

||ACC In-cluster|ACC Other-clusters|Equal Ratio|
|---|---|---|---|
|Cluster 1|0.9962|0.6286|0.9578|
|Cluster 2|0.7745|0.7071|0.8152|
|Cluster 3|0.9657|0.6384|0.8048|
|Cluster 4|0.8702|0.1850|0.5070|
|All|0.8734|0.5669|0.7712|




![](assets/cikm20/cikm20.pdf-0008-08.png)



![](assets/cikm20/cikm20.pdf-0008-09.png)


**(a) Positive Samples. (b) Negative Samples.** 

**Figure 4: Distribution visualization of intent vector** w **. We use** **_PCA_ to reduce the dimensions of** w **from** 16 **to** 2 **, and visualize the sample distribution of different clusters after normalization.** 

randomly select 5000 samples in each cluster. For each sample, we find its closest sample in other clusters in terms of _Euclidean distance_ , and we compare the labels of these two samples to find out whether advertisers with similar reports have the same satisfaction label. The results in the last column of Table 5 prove that even with similar advertising reports, advertisers’ satisfaction can be different due to the differences in intents. The only exception is the samples 

similar to Cluster 1, which has accuracy of 95.78%. This is because advertisers usually feel satisfied with ad units with good overall performance. 

The intent vector can be used as auxiliary information for downstream tasks. For example, we could use _w_ 1 _pCTR_ + _w_ 2 _pCVR_ + _w_ 3 _pCost_ as the ranking index in tag recommendation, where _pCTR_ , _pCVR_ and _pCost_ are the predicted indicators and _wi_ comes from the intent vector learned from advertisers. Weight average over indicators can also be used as the objective of real-time bidding algorithms. 

## **5.5 Online Evaluation** 

Our model can be deployed in different business scenarios related to advertiser satisfaction, such as whether an advertiser will be churned or not, whether the cost or take rate of an ad unit or advertiser will increase in the following week, or the advertiser’s attitude towards an adjust performance report. We have currently deployed our model as a key component in our online advertiser churn prediction system to serve different downstream optimization tasks, such as coupon distribution for unsatisfied advertisers, for more than four months. We use DSPN to predict the advertiser’s satisfaction of an advertiser over their all ad campaigns, which is a slight different from our offline setting, in which we use DSPN to predict the satisfaction over an ad unit. To overcome such a difference, we use the features like performance report and action information of an advertiser instead of an ad unit, to train DSPN model. The average AUC of DSPN for the advertiser churn prediction task in one month is around 0.9334 ± 0.0028. 

In online evaluation, we would get the actual churn result 10 days later based on the churn label, thus the training set and test set have a time gap of at least 10 days. To shed some light on the model’s performance at the moment, we randomly divide the data set into a training set and a validation set according to a 9 : 1 ratio. The average AUC in the validation set of the same 30 days is 0.9350 ± 0.0033, which is almost the same as the actual average AUC (0.9334 ± 0.0028). This result indicates that the model can well handle the performance loss caused by the time gap. In particular, our model has precision of 68.91% and recall of 51.96% in predicting the loyal advertisers who have consumption in the recent 10 days but will not have consumption in the next 10 days, which largely outperforms existing system’s main strategy, a rule-based method. In our nearest optimization through optimizing ad performance, the logging and recharging rate of 8500 advertisers increase by 0.7% and 1.0% respectively than 8500 homogeneous advertisers without optimization. 

## **6 Conclusion** 

In this paper, we have investigated the problem of advertiser intent learning and satisfaction prediction. Based on advertiser survey, empirical observations and mathematical analyses, we used a weight vector over advertising performance indicators to model the advertiser intent. Considering that the satisfied advertisers would continue to invest in ad campaigns, we proposed a metric related to the change of cost to evaluate the advertiser satisfaction. We then designed a deep learning network, namely DSPN, to identify advertiser intent and predict advertiser satisfaction, using the profile information of advertisers and ad units, performance indicators and sequential actions. Experimental results on an Alibaba advertisement dataset have shown the superiority of DSPN compared with the baseline models in terms of AUC and accuracy, and the effectiveness of using the weight vector to interpret the advertiser’s intent. DSPN has been deployed in the online advertiser churn prediction system in Alibaba, and has helped to avoid the unsatisfied advertisers to leave the ad platform. 

## **References** 

- [1] Dzmitry Bahdanau, Kyunghyun Cho, and Yoshua Bengio. 2014. Neural machine translation by jointly learning to align and translate. _arXiv preprint arXiv:1409.0473_ (2014). 

- [2] Benjamin Paul Chamberlain, Angelo Cardoso, CH Bryan Liu, Roberto Pagliari, and Marc Peter Deisenroth. 2017. Customer lifetime value prediction using embeddings. In _23rd SIGKDD_ . ACM, 1753–1762. 

- [3] Olivier Chapelle, Shihao Ji, Ciya Liao, Emre Velipasaoglu, Larry Lai, and SuLin Wu. 2011. Intent-based diversification of web search results: metrics and algorithms. _Information Retrieval_ 14, 6 (2011), 572–592. 

- [4] Heng-Tze Cheng, Levent Koc, Jeremiah Harmsen, Tal Shaked, Tushar Chandra, Hrishi Aradhye, Glen Anderson, Greg Corrado, Wei Chai, Mustafa Ispir, et al. 2016. Wide & deep learning for recommender systems. In _1st Workshop on DLRS_ . ACM, 7–10. 

user satisfaction with slate recommendations. In _28th WWW_ . 1256–1267. 

   - [19] Yanru Qu, Han Cai, Kan Ren, Weinan Zhang, Yong Yu, Ying Wen, and Jun Wang. 2016. Product-based neural networks for user response prediction. In _16th ICDM_ . IEEE, 1149–1154. 

   - [20] Saharon Rosset, Einat Neumann, Uri Eick, Nurit Vatnik, and Yizhak Idan. 2002. Customer lifetime value modeling and its use for customer retention planning. In _8th SIGKDD_ . ACM, 332–340. 

   - [21] Mike Schuster and Kuldip K Paliwal. 1997. Bidirectional recurrent neural networks. _IEEE transactions on Signal Processing_ 45, 11 (1997), 2673–2681. 

   - [22] Ying Shan, T Ryan Hoens, Jian Jiao, Haijing Wang, Dong Yu, and JC Mao. 2016. Deep crossing: Web-scale modeling without manually crafted combinatorial features. In _22nd SIGKDD_ . ACM, 255–262. 

   - [23] Humphrey Sheil, Omer Rana, and Ronan Reilly. 2018. Predicting purchasing intent: Automatic feature learning using recurrent neural networks. _arXiv preprint arXiv:1807.08207_ (2018). 

   - [24] Eugene Silberberg. 1972. Duality and the many consumer’s surpluses. _The American Economic Review_ 62, 5 (1972), 942–952. 

   - [25] Ning Su, Jiyin He, Yiqun Liu, Min Zhang, and Shaoping Ma. 2018. User intent, behaviour, and perceived satisfaction in product search. In _11th WSDM_ . ACM, 547–555. 

   - [26] Bhanu C Vattikonda, Santhosh Kodipaka, Hongyan Zhou, Vacha Dave, Saikat Guha, and Alex C Snoeren. 2015. Interpreting advertiser intent in sponsored search. In _21st SIGKDD_ . ACM, 2177–2185. 

   - [27] Hongning Wang, Yang Song, Ming-Wei Chang, Xiaodong He, Ahmed Hassan, and Ryen W White. 2014. Modeling action-level satisfaction for search task satisfaction prediction. In _37th SIGIR_ . ACM, 123–132. 

   - [28] Carl Yang, Xiaolin Shi, Luo Jie, and Jiawei Han. 2018. I Know You’ll Be Back: Interpretable New User Clustering and Churn Prediction on a Mobile Social Application. In _24th SIGKDD_ . ACM, 914–922. 

   - [29] Shuangfei Zhai, Keng-hao Chang, Ruofei Zhang, and Zhongfei Mark Zhang. 2016. Deepintent: Learning attentions for online advertising with recurrent neural networks. In _22nd SIGKDD_ . ACM, 1295–1304. 

   - [30] Guorui Zhou, Na Mou, Ying Fan, Qi Pi, Weijie Bian, Chang Zhou, Xiaoqiang Zhu, and Kun Gai. 2019. Deep interest evolution network for click-through rate prediction. In _33rd AAAI_ . 5941–5948. 

   - [31] Guorui Zhou, Xiaoqiang Zhu, Chenru Song, Ying Fan, Han Zhu, Xiao Ma, Yanghui Yan, Junqi Jin, Han Li, and Kun Gai. 2018. Deep interest network for click-through rate prediction. In _24th SIGKDD_ . ACM, 1059–1068. 

- [5] Junyoung Chung, Caglar Gulcehre, KyungHyun Cho, and Yoshua Bengio. 2014. Empirical evaluation of gated recurrent neural networks on sequence modeling. _arXiv preprint arXiv:1412.3555_ (2014). 

- [6] Paul Covington, Jay Adams, and Emre Sargin. 2016. Deep neural networks for youtube recommendations. In _10th RecSys_ . ACM, 191–198. 

- [7] David S Evans. 2008. The economics of the online advertising industry. _Review of Network Economics_ 7, 3 (2008). 

- [8] David S Evans. 2009. The online advertising industry: Economics, evolution, and privacy. _Journal of Economic Perspectives_ 23, 3 (2009), 37–60. 

- [9] Kun Gai, Xiaoqiang Zhu, Han Li, Kai Liu, and Zhe Wang. 2017. Learning piecewise linear models from large scale data for ad click prediction. _arXiv preprint arXiv:1704.05194_ (2017). 

- [10] Avi Goldfarb and Catherine Tucker. 2011. Online display advertising: Targeting and obtrusiveness. _Marketing Science_ 30, 3 (2011), 389–404. 

- [11] Huifeng Guo, Ruiming Tang, Yunming Ye, Zhenguo Li, and Xiuqiang He. 2017. DeepFM: a factorization-machine based neural network for CTR prediction. In _26th IJCAI_ . 1725–1731. 

- [12] Long Guo, Lifeng Hua, Rongfei Jia, Binqiang Zhao, Xiaobo Wang, and Bin Cui. 2019. Buying or Browsing?: Predicting Real-time Purchasing Intent using Attention-based Deep Network with Multiple Behavior. In _25th SIGKDD_ . ACM, 1984–1992. 

- [13] Sepp Hochreiter and Jürgen Schmidhuber. 1997. Long short-term memory. _Neural computation_ 9, 8 (1997), 1735–1780. 

- [14] Diederik P Kingma and Jimmy Ba. 2014. Adam: A method for stochastic optimization. _arXiv preprint arXiv:1412.6980_ (2014). 

- [15] Zachary C Lipton, John Berkowitz, and Charles Elkan. 2015. A critical review of recurrent neural networks for sequence learning. _arXiv preprint arXiv:1506.00019_ (2015). 

- [16] Yunfei Lu, Linyun Yu, Peng Cui, Chengxi Zang, Renzhe Xu, Yihao Liu, Lei Li, and Wenwu Zhu. 2019. Uncovering the Co-driven Mechanism of Social and Content Links in User Churn Phenomena. In _25th SIGKDD_ . ACM, 3093–3101. 

- [17] Rishabh Mehrotra, Ahmed Hassan Awadallah, Milad Shokouhi, Emine Yilmaz, Imed Zitouni, Ahmed El Kholy, and Madian Khabsa. 2017. Deep sequential models for task satisfaction prediction. In _26th CIKM_ . ACM, 737–746. 

- [18] Rishabh Mehrotra, Mounia Lalmas, Doug Kenney, Thomas Lim-Meng, and Golli Hashemian. 2019. Jointly leveraging intent and interaction signals to predict 

