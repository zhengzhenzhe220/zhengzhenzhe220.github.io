---
source: wiopt21.pdf
pages: 8
converter: pymupdf4llm
converted_at: 2026-08-30T22:11:43+08:00
---

# Data-Free Evaluation of User Contributions in Federated Learning 

Hongtao Lv<sup>_∗_</sup> , Zhenzhe Zheng<sup>_∗_</sup> , Tie Luo<sup>_†_</sup> , Fan Wu<sup>_∗_</sup> , Shaojie Tang<sup>_‡_</sup> , Lifeng Hua<sup>_§_</sup> , Rongfei Jia<sup>_§_</sup> , Chengfei Lv<sup>_§_</sup> 

_∗_ Shanghai Jiao Tong University _†_ Missouri University of Science and Technology 

_‡_ University of Texas at Dallas _§_ Alibaba Group 

Email: _{_ lvhongtao, zhengzhenzhe _}_ @sjtu.edu.cn, tluo@mst.edu, wu-fan@sjtu.edu.cn, shaojie.tang@utdallas.edu, _{_ issac.hlf, rongfei.jrf, chengfei.lcf _}_ @alibaba-inc.com 

**_Abstract_ —Federated learning (FL) trains a machine learning model on mobile devices in a distributed manner using each device’s private data and computing resources. A critical issues is to** **_evaluate individual users’ contributions_ so that (1) users’ effort in model training can be compensated with proper incentives and (2) malicious and low-quality users can be detected and removed. The state-of-the-art solutions require a representative test dataset for the evaluation purpose, but such a dataset is often unavailable and hard to synthesize. In this paper, we propose a method called** **_Pairwise Correlated Agreement_ (PCA) based on the idea of** **_peer prediction_ to evaluate user contribution in FL without a test dataset. PCA achieves this using the statistical correlation of the model parameters uploaded by users. We then apply PCA to designing (1) a new federated learning algorithm called Fed-PCA, and (2) a new incentive mechanism that guarantees truthfulness. We evaluate the performance of PCA and Fed-PCA using the MNIST dataset and a large industrial product recommendation dataset. The results demonstrate that our Fed-PCA outperforms the canonical FedAvg algorithm and other baseline methods in accuracy, and at the same time, PCA effectively incentivizes users to behave truthfully.** 

**_Index Terms_ —Peer prediction, correlated agreement.** 

## I. INTRODUCTION 

Recent years have seen a large variety of mobile applications that have changed or improved our ways of communication, shopping, commuting, traveling, and lifestyle. To provide personalized services in these applications, machine learning techniques have been increasingly adopted. For that purpose, a common practice is to upload user data to a central server or cloud, which then trains a machine learning model to make predictions such as product recommendation. This centralized approach evokes many privacy concerns as users’ sensitive data could be eavesdropped by malicious parties during data transmission, or be misused by an untrusted server. To address this privacy issue, a new learning paradigm called _Federated Learning_ (FL) [1] was proposed to perform distributed machine learning over a large number of devices 

This work was supported in part by China NSF grant No. 62025204, 62072303, 61972252, 61902248, and 61972254, in part by the National Science Foundation (NSF) under Grant CNS-2008878, in part by Shanghai Science and Technology fund 20PJ1407900, in part by Alibaba Group through Alibaba Innovation Research Program, and in part by Tencent Rhino Bird Key Research Project. The opinions, findings, conclusions, and recommendations expressed in this paper are those of the authors and do not necessarily reflect the views of the funding agencies or the government. 

Z. Zheng is the corresponding author. 

without requiring data to leave the devices or data owners. In the training process, each user trains a local model using her own data on her own device, and uploads the local model parameters instead of the original data to the server. The server then aggregates the received models into a global model and distributes the global model back to the users. The above steps repeat until the global model converges. By doing so, federated learning preserves user privacy and reduces network traffic. As a result, it has attracted substantial attention from both academia and industry recently. 

Unlike traditional distributed machine learning [2], in which the machines for model training are fully controlled by a central server, federated learning works with autonomous mobile users who decide by themselves whether and how to participate in model training. This makes FL vulnerable to selfish and malicious users who may manipulate the training process such as falsifying the model parameters or send random models without any training effort. Therefore, a critical issue in FL is to _evaluate individual users’ contributions_ in the model training process so that strategic users can be detected and truthful users can receive rewards proportional to their real contributions. 

A popular approach, as recently proposed in [3]–[5], uses the _Shapley value_ to measure user contribution in federated learning. This approach computes the marginal increase of average accuracy of the model due to the addition of data points contributed by a user in model training. However, this has two major drawbacks: 1) computing the Shapley value involves permutation operation which has an exponential computational complexity; even though some approximate methods have been proposed, the computation is still costly [4]; 2) more importantly, it relies on a representative test dataset to evaluate the model accuracy, but such a dataset is rarely available because no one knows which dataset perfectly mimics the distribution of future unseen data. 

To overcome these issues, we propose a _data-free_ approach to evaluate user contribution in FL. This approach only uses users’ uploaded models and does not need any extra training or test data. However, there are several key challenges. First, the uploaded models (typically neural networks) have complex structures and the correlation among model parameters is too intricate to express. Second, there may exist dishonest 

or malicious users who falsify their data or even directly manipulate model parameters [6], and detecting such behavior is hard because the server does not have access to user data. These challenges set the problem of evaluating user contribution in FL distinct from the data quality evaluation problem in mobile crowdsensing [7] and crowdsourcing [8]. 

To this end, we propose a _Pairwise Correlated Agreement_ (PCA) method to evaluate user contribution in FL. The basic idea is that, although the uploaded models are different among mobile users due to their non-i.i.d. (non-independent and identically distributed) data [9], we can still extract certain internal correlation between the models _pairwise_ , and exploit the correlation using an idea based on _peer prediction_ [10]. More specifically, we characterize user contribution by how much a model uploaded by a user can predict the models uploaded by the others via the internal correlations. 

With our PCA method, we apply it to two fundamental aspects of FL. First, we design a new _model aggregation_ algorithm called Fed-PCA, which uses the user contribution evaluation results as the model weights for model aggregation performed by the server. This Fed-PCA algorithm accounts for _quality_ of data, rather than just the user-reported data size (quantity); as a result, it offers significant potential to improve the accuracy of the aggregated model, and _counter the falsification of user-reported data size_ . Second, we apply PCA to designing an incentive mechanism which is strategy-proof to the following undesirable user behaviors: (i) _free riding_ , where a user randomly generates model parameters without performing the actual model training, and (ii) _overly privacypreserving_ : adding excessive noises to model parameters and thus substantially degrading model prediction performance. 

In summary, our main contributions are as follows: 

- We propose a Pairwise Correlated Agreement (PCA) method to evaluate user contributions in federated model training without using a test dataset. For motivation purposes, we also demonstrate the importance of contribution evaluation by showing the potential harm of strategic user behaviors on federated model training using our experiments conducted on an industrial dataset. 

- Based on PCA, we design an algorithm called Fed-PCA which uses the user contributions computed by PCA as the model weights in model aggregation. We also apply PCA to designing a strategy-proof incentive mechanism which resists two types of common strategic behaviors of users: free riding and overly privacy-preserving. 

- We conduct extensive experiments with the widely used MNIST dataset and an industrial dataset obtained from Taobao, one of the largest commercial mobile recommender system in China. The results clearly demonstrate the effectiveness of PCA in detecting users’ strategic behaviors. In addition, counter-intuitively, our Fed-PCA achieves equal or even better prediction accuracy as compared to FedAvg on different datasets, without knowing the training data size of each user. 

## II. PRELIMINARIES 

## _A. Federated Learning_ 

In the canonical FL framework [1], there is a set of users (clients) _U_ and a central server. Each user _i_ has a private local dataset _D_<sup>_i_</sup> , such as the historical dataset of click behaviors related to goods or videos in mobile recommender systems. In each round _t_ , _k_ users are randomly chosen to participate in the model training, and are denoted by the set _{_ 1 _, ..., k}_ . At the beginning of round _t_ , the server sends the global model **_M_** _t−_ 1 to the selected _k_ users, and each user trains a new local model **_M_**<sup>_i_</sup> _t_<sup>usingherowndata</sup><sup>_Di_,anduploadsthe</sup> model update **_x_**<sup>_i_</sup> _t_<sup>=</sup><sup>**_M_**</sup><sup>_i_</sup> _t_<sup>_−_</sup><sup>**_M_**</sup><sup>_t−_1totheserver.Besidesthe</sup> model update, each user also reports _n_<sup>_i_</sup> _t_<sup>,thesizeoftraining</sup> data used at round _t_ . The server then calculates the weight of each user _i_ as _wt_<sup>_i_=</sup><sup>_ni_</sup> _t_<sup>_/_�</sup><sup>_k_</sup> _j_ =1<sup>_n_</sup> _t_<sup>_j_,andaggregatesthemodel</sup> updates by **_<u>x</u>_** _t_ =<sup>�</sup><sup>_k_</sup> _i_ =1<sup>_w_</sup> _t_<sup>_i_</sup><sup>**_x_**</sup> _t_<sup>_i_.Finally,theglobalmodelis</sup> updated as **_M_** _t_ = **_M_** _t−_ 1 + **_<u>x</u>_** _t_ , which is sent back to users. The above process repeats until a stopping condition (e.g. a certain number of rounds) is met. As model compression with the quantization technique (e.g., [11]) is widely used in FL to reduce communication cost, we take each parameter of the model, indexed by _p_ , to be discrete and finite without loss of generality, i.e., _x_<sup>_i_</sup> _t,p_<sup>_∈{_1</sup><sup>_,_2</sup><sup>_, ..., h}_.Note,however,that</sup> our proposed approach can be used for continuous parameter values as well, in which case we can perform an additional quantization of the model update on the server only for the contribution evaluation phase, and it does not affect the model aggregation (i.e., the model update of each user _i_ does not need to be quantized in the model aggregation). 

## _B. Undesirable User Strategies_ 

In an ideal FL framework, each user would participate in the model training, upload her model truthfully. However, there may exist strategic users who can manipulate this process to achieve their own interests, e.g., by uploading a fake model update **_x_** ˆ<sup>_i̸_</sup> = **_x_**<sup>_i_</sup> where **_x_**<sup>_i_</sup> is the true model update (omitting subscript _t_ for notation simplicity). We account for two main types of strategic user behaviors in FL: 1) free riding [6], which generates random model parameters without actually training to save training costs, such as computing power and storage; and 2) overly privacy-preserving, which adds excessive noises to the model parameters for privacy protection [11]–[13]). 

To observe the effects of these strategic behaviors on the model training in FL, we have conducted two experiments on Deep Interest Network (DIN) [14], a deep learning-based click-through rate (CTR) prediction model, with an industrial dataset from Taobao. We adopt the classic performance metric in machine learning: area under the curve (AUC), and the baseline of AUC is 0.5. The detailed experimental setup can be found in Section V-B. In Fig. 1(a), we investigate the effect of free riders, where a free rider randomly generate her model parameter _x_ ˆ<sup>_i_</sup> _p_<sup>_∼N_(0</sup><sup>_, σ_</sup> 1<sup>2),i.e.,theGaussiandistributionwith</sup> variance _σ_ 1 = 0 _._ 01. As shown in Fig. 1(a), just 25% free riders are enough to degrade the performance substantially. In Fig. 


![](assets/wiopt21/wiopt21.pdf-0003-00.png)



![](assets/wiopt21/wiopt21.pdf-0003-01.png)


<!-- Start of picture text -->
(a) (b)<br><!-- End of picture text -->

Fig. 1: Performance in terms of area under the curve (AUC) with two types of strategic users: (a) free riders in different percentages, (b) privacy-preserving users in different noise scales _σ_ 2. 

1(b), we investigate the performance with privacy-preserving behaviors. Each user further strengthen the privacy by adding noises into the model parameters, i.e., _x_ ˆ<sup>_i_</sup> _p_<sup>=</sup><sup>_x_</sup> _p_<sup>_i_+</sup><sup>_N_(0</sup><sup>_, σ_</sup> 2<sup>2),</sup> where _N_ (0 _, σ_ 2<sup>2)isGaussiandistributionwithvariance(noise</sup> scale) _σ_ 2. The result in Fig. 1(b) shows that the AUC depends heavily on the noise scale _σ_ 2: when _σ_ 2 = 0 _._ 001, the performance has a slight degradation, but when _σ_ 2 = 0 _._ 01 or larger, the AUC drops significantly, which demonstrates the harmfulness of overly privacy-preserving behaviors (due to excessive noise). With these observations, a contribution evaluation method is highly needed to detect and suppress the free riding behaviors and overly privacy-preserving behaviors. 

To formulate the above strategic behaviors in a unified manner, we define the strategy of a user as _Fr,a_ = _P_ (ˆ _xp_ = _r|xp_ = _a_ ) for any _r, a ∈{_ 1 _,_ 2 _, ..., h}_ and parameter _p_ , where _r_ is the reported parameter value and _a_ is the true value.<sup>1</sup> In other words, the strategy is the probability of reporting _r_ when the value of parameter _p_ is _a_ . Next, we formulate the above behaviors as informed and uninformed strategies. 

**Definition 1** ( **Informed and Uninformed Strategies** ) **.** _A strategy is an uninformed strategy if it has Fr,a_ = _Fr,b for any r, a, b ∈{_ 1 _,_ 2 _, ..., h}, otherwise is an informed strategy if there exists Fr,a̸_ = _Fr,b for some r, a, b, it is an informed strategy._ 

Intuitively, the uninformed strategy captures the free-rider behaviors, where the user does not spend resources or effort in training the model, but just report some random parameter values. Hence, the probability of the reported values does not depend on the true values. On the other hand, the informed strategy captures the privacy-preserving behaviors where the user has indeed trained the local model using her local data, but then obfuscated the true parameter value _x_<sup>_i_</sup> _p_<sup>into a reported</sup> value _x_ ˆ<sup>_i_</sup> _p_<sup>withsomeprobability.Notethattruthfullyreporting</sup> model updates is also an informed strategy, where _Fa,a_ = 1 and _Fr,a_ = 0 _, ∀r̸_ = _a_ . 

1Another possibility is to consider the probability conditional on parameter index _p_ . However, it is usually not possible for a user to figure out the relation between a particular parameter in a neural network and her own interest, due to the complex structure of neural network models. 

## _C. Peer Prediction and Correlated Agreement_ 

First introduced in [15], the peer-prediction method is a classic mechanism for information elicitation problems without a ground truth, and has been employed in many scenarios, such as crowdsourcing [16] and peer grading [17]. The key idea of peer prediction is to compare the reported data of user _i_ with that of other users. If their data satisfy some statistical correlation, i.e., the data of user _i_ is predictive of the data of others, then her data is deemed to have a larger contribution, and vice versa. Peer prediction is naturally suitable for FL since there is no ground truth for the contribution evaluation. 

For consistency with the terminology used in the peerprediction literature, we also call each parameter in a FL model, indexed by _p_ , a _task_ . Each user fulfills a task by training the parameter with her private local data (using, e.g., the gradient descent algorithm). Note that in FL, the task set of each user is the same since all the users are training the same model. We call the value after performing the training task, _x_<sup>_i_</sup> _p_<sup>,</sup> a _signal_ , whereby each signal belongs to the set _{_ 1 _,_ 2 _, ..., h}_ . 

Next, we define a _delta matrix_ ∆, which is an _h × h_ matrix that captures the correlation between each pair of users on a certain task. We first consider the case of homogeneous user, i.e., the delta matrix is the same for each pair of the users. Thus, we omit the user index for the delta matrix. Let _P_ ( _a, b_ ) denote the joint probability that one user gets signal _a_ after training and the other user gets signal _b_ on the same parameter, and _P_ ( _a_ ) and _P_ ( _b_ ) denote the corresponding marginal probabilities. An entry ∆( _a, b_ ) is then defined as 

## ∆( _a, b_ ) ≜ _P_ ( _a, b_ ) _− P_ ( _a_ ) _P_ ( _b_ ) _._ 

If ∆( _a, b_ ) _>_ 0, we have that the signals _a_ and _b_ are positively correlated; if ∆( _a, b_ ) = 0, we have that _a_ and _b_ are independent; otherwise, they are negatively correlated. In addition, it can be easily verified that the sum of ∆( _a, b_ ) in each row or each column is always 0. We define _Sign_ (∆( _a, b_ )) = 1 if ∆( _a, b_ ) _>_ 0, and _Sign_ (∆( _a, b_ )) = 0 otherwise. Without loss of generality, we assume that there is at least one element in the matrix that is non-zero. 

With the above definitions, we describe the _correlated agreement_ (CA) method introduced by [10], [17] in the context of FL. 

**Definition 2** ( **CA Method for Homogeneous Users** ) **.** _The CA method entails the following steps:_ 

- _1) Randomly divide the parameters into a bonus parameter set M_ 1 _and a penalty parameter set M_ 2 _._ 

- _2) For each user i and each bonus parameter p ∈ M_ 1 _, randomly pick a user j̸_ = _i as the_ peer _of i, and randomly choose two different penalty parameters q, q_<sup>_′_</sup> _∈ M_ 2 _for users i and j, respectively._ 

- _3) The contribution or quality of parameter p of user i is evaluated by Q_<sup>_i_</sup> _p_<sup>=</sup><sup>_S_(ˆ</sup><sup>_xi_</sup> _p_<sup>_,_ˆ</sup><sup>_xj_</sup> _p_<sup>)</sup><sup>_−S_(ˆ</sup><sup>_xi_</sup> _q_<sup>_,_ˆ</sup><sup>_xj_</sup> _q_<sup>_′_)</sup><sup>_,wherethe_</sup> _score matrix is S_ = _Sign_ (∆) _, and user i’s contribution is Q_<sup>_i_</sup> = _|M_ <u>11</u> _|_ � _p∈M_ 1<sup>_Q_</sup> _p_<sup>_i._</sup> 

## **Algorithm 1:** ComputeDelta( _i, j, A, B_ ) 

**Input:** The focus user _i_ , the peer user _j_ , and the parameter sets _A_ and _B_ . **Output:** The delta matrices ∆<sup>_i,j_</sup> _A_<sup>_,_∆</sup><sup>_i,j_</sup> _B_<sup>.</sup> **1 for** _each pair of signals a, b ∈{_ 1 _,_ 2 _, ..., h}_ **do** <u>�</u> _<u>p∈A</u>_<sup>**1**(ˆ</sup><sup>_x_</sup> _<u>p</u>_<sup>_i_=</sup><sup>_a,x_ˆ</sup><sup>_j_</sup> _<u>p</u>_<sup>=</sup><sup>_b_)</sup> **2** _TA_<sup>_i,j_(</sup><sup>_a, b_)</sup><sup>_←_</sup> _|A|_ . <u>�</u> _<u>p∈A</u>_<sup>**1**(ˆ</sup><sup>_x_</sup> _<u>p</u>_<sup>_i_=</sup><sup>_a_)</sup> **3** _TA_<sup>_i_(</sup><sup>_a_)</sup><sup>_←_</sup> _|A|_ . <u>�</u> _<u>p∈A</u>_<sup>**1**(ˆ</sup><sup>_x_</sup> _<u>p</u>_<sup>_j_=</sup><sup>_b_)</sup> **4** _TA_<sup>_j_(</sup><sup>_b_)</sup><sup>_←_</sup> _|A|_ . **5** Repeat Lines 1 - 4 for parameter set _B_ . **6 for** _each pair of signals a, b ∈{_ 1 _,_ 2 _, ..., h}_ **do 7** ∆<sup>_i,j_</sup> _A_<sup>(</sup><sup>_a, b_)</sup><sup>_←T i,j_</sup> _A_<sup>(</sup><sup>_a, b_)</sup><sup>_−T i_</sup> _A_<sup>(</sup><sup>_a_)</sup><sup>_T j_</sup> _A_<sup>(</sup><sup>_b_).</sup> **8** ∆<sup>_i,j_</sup> _B_<sup>(</sup><sup>_a, b_)</sup><sup>_←T i,j_</sup> _B_<sup>(</sup><sup>_a, b_)</sup><sup>_−T i_</sup> _B_<sup>(</sup><sup>_a_)</sup><sup>_T j_</sup> _B_<sup>(</sup><sup>_b_).</sup> 

The intuition in Step 3 is that if the reported signals by user _i_ and her peer _j_ on the same parameter _p_ exhibit a positive statistical correlation (e.g., they both report _a_ as in the above example), we give user _i_ a reward of 1. On the other hand, if their signals on two different parameters _q_ and _q_<sup>_′_</sup> are positively correlated, it suggests that the user _i_ may have randomly uploaded an arbitrary signal for each parameter without actual training, so we give her a penalty of _−_ 1. 

**Algorithm 2:** Pairwise Correlated Agreement (PCA) Method for Heterogeneous Users 

**Input:** The set of selected users _Kt_ , the reported model updates **_x_** ˆ<sup>_i_</sup> of each user _i ∈ Kt_ , and the number of peers _m_ . **Output:** The contribution _Q_<sup>_i_</sup> of each user _i ∈ Kt_ . **1** Randomly divide model parameters into bonus parameter set _M_ 1 and penalty parameter set _M_ 2. **2 for** _each user i ∈ Kt_ **do 3** _PR_<sup>_i_</sup> _←_ (a set of randomly selected _m_ users in _Kt\i_ as peers). **4 for** _each peer j ∈ PR_<sup>_i_</sup> **do 5** Randomly divide parameters into two sets _A, B_ of the same size. **6** ∆<sup>_i,j_</sup> _A_<sup>_,_∆</sup><sup>_i,j_</sup> _B_<sup>_←_ComputeDelta(</sup><sup>_i, j, A, B_).</sup> **7 for** _each parameter p ∈ M_ 1 _∩ A_ **do 8** Randomly choose two different parameters _q, q_<sup>_′_</sup> _∈ M_ 2 _∩ A_ . **9** _Q_<sup>_i,j_</sup> _p ← Sign_ (∆<sup>_i,j_</sup> _B_<sup>(ˆ</sup><sup>_xi_</sup> _p_<sup>_,_ˆ</sup><sup>_xj_</sup> _p_<sup>))</sup><sup>_−Sign_(∆</sup> _B_<sup>_i,j_(ˆ</sup><sup>_xi_</sup> _q_<sup>_,_ˆ</sup><sup>_xj_</sup> _q_<sup>_′_)).</sup> **10** Repeat Lines 7 - 9 for each parameter _p ∈ M_ 1 _∩ B_ with ∆<sup>_i,j_</sup> _A_<sup>.</sup> <u>1</u> **11** _Q_<sup>_i_</sup> _← m|M_ 1 _|_ <u>�</u> _p∈M_ 1 <u>�</u> _j∈P R_<sup>_i Q_</sup> _p_<sup>_i,j_.</sup> 

## III. PAIRWISE CORRELATED AGREEMENT (PCA) 

The above CA method assumes that all the users are homogeneous, and the delta matrix is the same for all the user pairs. However, one distinctive feature of FL is that users are heterogeneous with non-i.i.d. or imbalanced data [1]. For instance, in mobile recommender systems, the click behaviors of users can be substantially different. The work [18] extended the CA method to the heterogeneous users setting, which divides users into several groups and computes the delta matrix for each pair of groups. However, when there are a large number of heterogeneous users, which is likely to occur in FL, the number of groups would be quite huge, and then this method suffers from a prohibitive computing complexity for both the clustering procedure and the calculation of delta matrices. To address this issue, we propose a _pairwise correlated agreement_ (PCA) method, and explores the underlying internal correlation of signal distributions to evaluate the contribution of heterogeneous users. 

Before introducing PCA, we make a reasonable assumption that the signal of different parameters are independent and identically distributed (i.i.d.), which is based on our observation from practical data sets. To validate this assumption, we again conduct two experiments on DIN with an industrial dataset from taobao. We first test the _Spearman’s Correlation_ [19] between the signals of two randomly chosen parameters to validate the independence hypothesis. Second, we conduct the _Kolmogorov-Smirnov Test_ [20] between them to validate the hypothesis of identical distribution. The resulting _p_ -values are 0.185 and 0.343, respectively, and both of them are larger than 0.05, which adequately supports the i.i.d. assumption. We 

note that this assumption is also used in many related works on sensitivity analysis of neural networks [21]–[23]. 

Under this assumption, we conduct Algorithm 1 to estimate the delta matrix for each pair of heterogeneous users. As shown later in the proof of Theorem 1, the estimation error could be arbitrarily small with a large number of samples. In algorithm 1, parameters are split into two sets, _A, B_ , of the equal size, and we compute a delta matrix for each parameter set and each pair of user _i_ and her peer _j_ . The function **1** ( _·_ ) in Lines 2 to 4 denotes the indicator function. We use _TA_<sup>_i,j_(</sup><sup>_a, b_)</sup> as the observed frequency of jointly reporting _a, b_ from users _i, j_ for the parameter set _A_ , and _TA_<sup>_i_(</sup><sup>_a_)and</sup><sup>_T j_</sup> _A_<sup>(</sup><sup>_b_)asthe</sup> corresponding marginal probabilities (Lines 1 - 5). Lines 6 - 8 compute the delta matrix of each parameter set _A_ and _B_ . Then, PCA is given in Algorithm 2. For each focus user _i_ , we randomly choose _m_ peers (Line 3). With a larger _m_ , the accuracy of _Q_<sup>_i_</sup> could be improved while the expectation remains the same since we would take the average among them. Then, for each parameter set _A, B_ of user _i_ and her peer _j_ , we apply Algorithm 1 to obtain different estimated delta matrices ∆<sup>_i,j_</sup> _B_<sup>and∆</sup><sup>_i,j_</sup> _A_<sup>,respectively(Lines5-6).Notethat</sup> we use swapped statistical correlations, i.e., the delta matrices, to calculate the score matrix _Q_ (Line 9). As such, the score matrix is independent of the reported parameters themselves.<sup>2</sup> 

> 2To understand this, suppose a signal _r_ occurs only once on parameter _p_ . Then since we compute the delta matrix statistically, the signal _r_ will always receive a reward of 1 on this parameter because the correlation is calculated with itself. 

**Algorithm 3:** Fed-PCA: An improved FL aggregation algorithm using weights calculated by PCA 

**Input:** The set of users _U_ , the initialized model **_M_** 0, the number of learning rounds _T_ . **Output:** The global model **_M_** _T_ . **1 for** _each round t ∈{_ 1 _,_ 2 _, ..., T }_ **do 2** _Kt ←_ (a set of _k_ users randomly selected from _N_ ). **3 for** _each user i ∈ Kt_ **_in parallel_ do 4** Obtain new local model **_M_**<sup>_i_</sup> _t_<sup>andmodelupdate</sup> **_x_**<sup>_i_</sup> = **_M_**<sup>_i_</sup> _t_<sup>_−_</sup><sup>**_M_**</sup><sup>_t−_1.</sup> **5** Report **_x_** ˆ<sup>_i_</sup> to the server. **6** Get the contribution _Q_<sup>_i_</sup> for each user _i ∈ Kt_ by Algorithm 2. **7 for** _each user i ∈ Kt_ **do 8** _w_<sup>_i_</sup> _←_ exp( _αQ_<sup>_i_</sup> ) _/_<sup>�</sup><sup>_k_</sup> _j_ =1<sup>exp(</sup><sup>_αQj_).</sup> **9 for** _each parameter p in the model_ **do 10** _<u>xp</u> ← w_<sup>_i_</sup> _x_ ˆ<sup>_i_</sup> _p_<sup>.</sup> **11** **_M_** _t ←_ **_M_** _t−_ 1 + **_<u>x</u>_** <u>.</u> 

Lastly, we compute the overall contribution of user _i_ ’s model update in Line 11. 

Intuitively, PCA estimates and takes advantage of the correlation between the uploaded models of heterogeneous users. 

## IV. APPLICATIONS OF PCA 

In this section, we describe two potential applications of PCA: weight calculation in model aggregation and incentive mechanism design. 

## _A. Weight Calculation for Model Aggregation_ 

In order to reduce the negative effects of low-quality uploaded models, we leverage the contribution value provided by PCA in model aggregation and propose the improved FL algorithm called Fed-PCA. In particular, Fed-PCA aims to achieve two goals: 1) to prevent falsification of the data size _n_<sup>_i_</sup> , which is a serious issue in FL since it directly affects the weights in model aggregation; 2) to improve the performance of FL as the traditional model aggregation does not take into account the model/data contribution of users. 

As shown in Algorithm 3, we map the value of user _i_ ’s contribution from the interval [ _−_ 1 _,_ 1] to a non-negative weight _w_<sup>_i_</sup> = exp( _αQ_<sup>_i_</sup> ) _/_<sup>�</sup><sup>_k_</sup> _j_ =1<sup>exp(</sup><sup>_αQj_)inLine8.Here,weuse</sup> the exponential function with a controlled parameter _α_ , which determines the variance of user weights in model aggregation. The local models are then aggregated into the global model using the new normalized user weights (Lines 9 - 11). Note that our contribution values could be used in not only the weighted averaging aggregation process as shown here, but also the recent median-based mechanisms proposed to defend Byzantine attacks [24], [25]. We evaluate the performance for both the averaging and median-based aggregation methods in Section V. 

## _B. Incentive Mechanism Design_ 

We next discuss how to prevent the strategic behaviors through incentives, where an essential property for this issue is _incentive compatibility_ . We say that incentive compatibility is satisfied when it is in all users’ best interests (obtaining the highest rewards) to report their true models, i.e., 


![](assets/wiopt21/wiopt21.pdf-0005-11.png)


for any reported **_x_** ˆ<sup>_i_</sup> , where _U_<sup>_i_</sup> denotes the utility obtained by user _i_ , which will be defined later, and _{_ **_x_** ˆ<sup>_j_</sup> _}_<sup>_j̸_=</sup><sup>_i_</sup> is the set of reported model updates of all the other users. We emphasize that incentive compatibility could be quite important for FL, because otherwise, users may upload falsified models and the learning problem would be ill-defined. 

Next, based on the definition of informed and uninformed strategies in Section II-B, we introduce the concept of informed incentive compatibility and _ϵ_ -informed incentive compatibility for the above defined strategic behaviors. We denote by I<sup>_i_</sup> and _{_ I _}_<sup>_j̸_=</sup><sup>_i_</sup> the truthful strategy of user _i_ and that of other users, respectively. 

**Definition 3** ( **Informed Incentive Compatibility and** _ϵ_ **-Informed Incentive Compatibility** ) **.** _If for every user i and any informed strategies F, G, and some ϵ ≥_ 0 _, we have_ 


![](assets/wiopt21/wiopt21.pdf-0005-15.png)


_and for any uninformed strategy F_<sup>_′_</sup> _, we have_ 


![](assets/wiopt21/wiopt21.pdf-0005-17.png)


_then the mechanism is ϵ-informed incentive compatible. If ϵ_ = 0 _, the mechanism is informed incentive compatible._ 

The definition of _ϵ_ -informed incentive compatibility reflects that (i) if a user adopts an uninformed strategy, her contribution is strictly lower than that of truthful reporting; (ii) if a user adopts an informed (yet still untruthful) strategy, her contribution is at best _ϵ_ more than that of truthful behavior, where _ϵ_ is a small constant number. Therefore, an incentive mechanism with this property can prevent strategic users from uninformed or informed strategies. 

Aiming to illustrate the application of PCA in a clearest manner, we assume that the utility of each user is simply her received reward, regardless of other factors, that is, _U_<sup>_i_</sup> (ˆ **_x_**<sup>_i_</sup> _, {_ **_x_** ˆ<sup>_j_</sup> _}_<sup>_j̸_=</sup><sup>_i_</sup> ) = _R_<sup>_i_</sup> (ˆ **_x_**<sup>_i_</sup> _, {_ **_x_** ˆ<sup>_j_</sup> _}_<sup>_j̸_=</sup><sup>_i_</sup> ) where _R_<sup>_i_</sup> (ˆ **_x_**<sup>_i_</sup> _, {_ **_x_** ˆ<sup>_j_</sup> _}_<sup>_j̸_=</sup><sup>_i_</sup> ) is the reward received by user _i_ . It should be noted that PCA could be easily integrated into most of other existing incentive mechanisms, such as that in [26], [27], and more factors could be taken into account, e.g., the training cost, the privacy cost and the budget balance property. 

On top of this simplified utility model of users, we propose that the following simple mechanism could guarantee the _ϵ_ -informed incentive compatibility: allocating a reward = proportional to her contribution, i.e., _R_<sup>_i_</sup> (ˆ **_x_**<sup>_i_</sup> _, {_ **_x_** ˆ<sup>_j_</sup> _}_<sup>_j̸_=</sup><sup>_i_</sup> ) _f_ ( _Qi_ (ˆ **_x_**<sup>_i_</sup> _, {_ **_x_** ˆ<sup>_j_</sup> _}_<sup>_j̸_=</sup><sup>_i_</sup> )) where _f_ could be any positive monotonic increasing function. We posit the following main theorem, 


![](assets/wiopt21/wiopt21.pdf-0006-00.png)



![](assets/wiopt21/wiopt21.pdf-0006-01.png)


<!-- Start of picture text -->
(a) (b)<br><!-- End of picture text -->

Fig. 2: Results on MNIST with free-riding users: (a) Average weight assigned to free-riding users; (b) Test accuracy. 

(a) (b) 

Fig. 3: Results on MNIST with (overly) privacy-preserving users: (a) Average weight assigned to privacy-preserving users. (b) Test accuracy with 25% privacy-preserving users. 

which shows that this mechanism is close to informed incentive compatibility. 

**Theorem 1.** _Let ϵ >_ 0 _, and δ >_ 0 _. If the number of samples is g_ = _O_ (9 _h_<sup>2</sup> log(1 _/δ_ ) _/ϵ_<sup>2</sup> ) _, then with a probability of at least_ 1 _−δ, the above incentive mechanism with heterogeneous users is ϵ-informed incentive compatible._ 

We omit the proof due to space constraint. 

## V. PERFORMANCE EVALUATION 

In this section, we report the evaluation results of our proposed approach and methods (PCA, Fed-PCA, and incentive mechanism) using the MNIST dataset and an industrial product recommendation dataset. 

## _A. Experiments on the MNIST Dataset_ 

**Experimental Setting.** We first study the performance of Fed-PCA for the MNIST digit-recognition dataset using a multi-layer perceptron with a hidden layer of 100 units. ReLU activations and dropout technique are adopted in the experiments. The network contains a total of 159,010 parameters. Similar to [1], we first sort the MNIST data by digit label, and divide them into 200 shards, each of which includes 300 data items. We assume there are 100 users in total in the FL system, each of which is randomly assigned two shards of data. This way, the data distribution among users is highly non-i.i.d.<sup>3</sup> 

For the model updates, we choose a gradient quantization technique called cpSGD [11] to reduce the communication cost. In the FL training, _k_ = 20 users are randomly chosen in one round. We adopt mini-batch stochastic gradient descent (SGD) with momentum as the optimization algorithm. The value of momentum is set to 0.5, the batch size is 10, the local epoch number in each round is 5, and the learning rate is 0.01. In the quantization process, we set _h_ = 8, and _X_<sup>_max_</sup> = 0 _._ 1. In PCA, the peer number _m_ is 5, and the number of bonus parameters is _|M_ 1 _|_ = 1 _,_ 000. The parameter _α_ , which converts the user contribution into her weight, is set to 10. Regarding the free riders in the system, we assume the parameters they 

> 3Following [1], we adopt this balanced partition, but in our experiments on the industrial dataset, users are divided naturally in an unbalanced manner. 

generate in their model updates to be _x_ ˆ<sup>_i_</sup> _p_<sup>=</sup><sup>_N_(0</sup><sup>_, σ_</sup> 1<sup>2),where</sup> _σ_ 1 is set to 0.01. In the experiments on privacy-preserving users, we assume that 25% of users add noises into their model parameters, each of which reports _x_ ˆ<sup>_i_</sup> _p_<sup>=</sup><sup>_xi_</sup> _p_<sup>+</sup><sup>_N_(0</sup><sup>_, σ_</sup> 2<sup>2).We</sup> will test the impact of different noise scales _σ_ 2. 

**Experimental Results.** We first compare the performance of our Fed-PCA with the original FedAvg algorithm with different percentages of free riders. For clarity, we illustrate the user contributions using their corresponding weights, as calculated in Algorithm 3. Fig. 2(a) shows the average weight of free riders. When the percentage of free riders is no more than 20%, PCA evaluates their contributions (and hence weights) as nearly 0, while FedAvg constantly assigns them a weight of 0.05 (recall there are 20 users). This result demonstrates that free riders are detected accurately by PCA, while further implying the effectiveness of our incentive mechanism. When the percentage of free riders increases to 50%, their average weight increases accordingly, but is always lower than that of FedAvg. This is because that the model quality of peers decreases with the percentage of free riders. Note that we could assume most users in FL are likely to be truthful, which provides a reference to detect free riders. This is a mild assumption in real life and has been widely adopted in previous literature [6], [28]. In Fig. 2(b), we study the test accuracy with different percentages of free riders. It is depicted in the figure that Fed-PCA decisively outperforms the FedAvg algorithm. The reason is that PCA detects free riders successfully and, thus, assigns them low weights in the model aggregation process. We also note that in the normal case without any free riders or privacy-preserving users, the accuracy of Fed-PCA is 0.9421 after 100 rounds, which is quite close to the baseline of FedAvg: 0.9458. 

The impact of the noise scale _σ_ 2 of privacy-preserving users is shown in Fig. 3. Fig. 3(a) explores the average weight of privacy-preserving users. When the noise scale _σ_ 2 is no less than 0.05, the average weight of privacy-preserving users is nearly 0, while a lower noise scale leads to a higher weight. This result demonstrates that PCA is capable of detecting users who add large noises, but ignores the slight noises that do not affect the performance of FL, which is a good characteristic 


![](assets/wiopt21/wiopt21.pdf-0007-00.png)



![](assets/wiopt21/wiopt21.pdf-0007-01.png)


<!-- Start of picture text -->
(a) (b)<br><!-- End of picture text -->

Fig. 4: Results on industrial dataset: (a) Average weight assigned to free-riding users. (b) Average weight assigned to privacy-preserving users. 


![](assets/wiopt21/wiopt21.pdf-0007-03.png)


<!-- Start of picture text -->
0.58<br>0.57<br>0.56<br>0.55<br>0.54<br>0.53<br>0.52 Fed-PCA<br>FedAvg<br>0.51 Med-PCA<br>0.50 Med<br>0 1000 2000 3000 4000 5000<br>Round<br>AUC<br><!-- End of picture text -->

Fig. 5: Comparison of different model aggregation methods. 

of the corresponding incentive mechanism. In Fig. 3(b), we show the test accuracy of Fed-PCA and FedAvg. The accuracy of FedAvg degrades seriously with the increase of _σ_ 2, but our Fed-PCA remains nearly unaffected by users with large noises because they are assigned very low weights. 

## _B. Experiments on the Industrial Dataset_ 

**Experimental Setting.** We next evaluate the performance of our Fed-PCA on an industrial dataset from Taobao, one of the largest a mobile recommendation system of products in China. In the dataset, there are 30-day impressions and click logs of users (dated from June 15 to July 15, 2019). We use the Deep Interest Network (DIN) [14] as the machine learning models. We refer the readers to [14] for more details on DIN and the dataset. 

In the training of FL, the batch size is set to 2, the epoch number is set to 1, and the learning rate is initialized as 1.0 with an exponential decay rate of 0.999. In the quantization process, we set _h_ = 256, and set _X_<sup>_max_</sup> as 0.1 multiplied by the learning rate in the round. In PCA, the parameter _α_ is set to 100 if not otherwise stated. The other parameters are the same as those of the experiments on the MNIST dataset. 

**Experimental Results.** We first explore the average weight of free riders and privacy-preserving users in Fig. 4. In Fig. 4(a), we can see that when the percentage of free riders is no more than 30%, all of them are detected in PCA and, hence, are allocated merely 0 weight in the aggregation. When the percentage increases to 50%, Fed-PCA still has the ability 

to detect them to some extent; thus, their average weight is about half that of truthful users. We investigate the impact of privacy-preserving users in Fig. 4(b). A clear noise scale boundary of 0.001 is found, above which the user would be detected and punished with a low weight. These results clearly suggest the effectiveness of PCA in the application of incentive mechanism design. 

Then, we test the AUC with different aggregation methods in the system consisting of exclusively truthful users in Fig. 5. As median-based aggregation methods has attracted much attention in recent years as resistant to the attacks of malicious users [24], [28], we conduct experiments on both averaging and median aggregation. In the figure, the black line (Med) is the performance of the unweighted median-based aggregation method, and the red line (Med-PCA) represents a mix of PCA and the weighted median methods. It is depicted that the unweighted median-based aggregation method underperforms all other approaches since more information of the model updates from the users are lost due to the median operation, compared with the averaging operation. PCA helps alleviate this problem by allocating larger weights to the users with better performance in the median operation. Surprisingly, we can observe that, under the premise of preventing free riders and overly privacy-preserving users, the performance of FedPCA clearly surpasses all other aggregation methods, including FedAvg. This means that the contributions and, hence, the weights calculated by PCA are even more reasonable and effective than the traditional weights directly calculated by data sizes, in absence of the information about local datasets. We conjecture that this is because of the difference between the synthetic MNIST dataset and the industrial dataset. In MNIST, each data item has approximately the same value for the learning problem, and hence the data sizes could be used as a good proxy of weights in model aggregation. But in the industrial dataset, real users may provide many useless data items for the learning problem, such as unintended activations. Therefore, a well-designed weight assignment approach has the potential to evaluate the true contribution of each user, and hence to outperform the traditional FL algorithm. 

## VI. RELATED WORK 

The FL framework was first introduced by Google [1], [29] as a new paradigm of distributed machine learning, and it has been applied in a virtual keyboard named Gboard [30], [31]. Some recent works have taken incentive mechanisms of FL into account [3], [4], [26], [27], [32], [33]. For example, [34] proposes an incentive mechanism for FL using the contract theory, by considering the computation and communication costs of training the model. These studies focused on the costs of users, while the contribution of each user to the FL platform is simplified as a sandbox or a linear function of her cost, which is not so practical in real life. Some other work [3]–[5] account for the contribution using the Shapley valuebased techniques. However, as stated above, the computation of Shapley values suffers from high time complexity and the requirement of a representative test dataset in FL, which 

poses obstacles for fair contribution evaluation. Closely related works are [35], [36], which adopt peer prediction to compare the output of the updated models of users on the test data, and thus a representative test dataset is still required in their proposed approaches. Our work tackles this problem by leveraging the technique of peer prediction on the model parameters, whereby the contribution of each user is evaluated without either training data or test data. 

## VII. CONCLUSION 

In this paper, we have proposed a pairwise correlated agreement (PCA) method to evaluate the contributions of users in federated learning, without requiring a test dataset. We have then applied PCA in (1) weight calculation for more robust model aggregation, where we have designed Fed-PCA as a better alternative to FedAvg, and (2) incentive mechanism design for FL. Extensive experiments are conducted using the MNIST dataset and a large industrial product recommendation dataset. The evaluation results demonstrate the effectiveness of our proposed approach in terms of both detecting strategic user behaviors and improving prediction accuracy. 

## REFERENCES 

- [1] H. B. McMahan, E. Moore, D. Ramage, S. Hampson _et al._ , “Communication-efficient learning of deep networks from decentralized data,” in _AISTAT_ , 2017. 

- [2] J. Qiu, Q. Wu, G. Ding, Y. Xu, and S. Feng, “A survey of machine learning for big data processing,” _EURASIP Journal on Advances in Signal Processing_ , vol. 2016, no. 1, p. 67, 2016. 

- [3] Y. Liu, S. Sun, Z. Ai, S. Zhang, Z. Liu, and H. Yu, “Fedcoin: A peer-to-peer payment system for federated learning,” _arXiv preprint arXiv:2002.11711_ , 2020. 

- [4] R. Jia, D. Dao, B. Wang, F. A. Hubis, N. Hynes, N. M. Gurel, B. Li, C. Zhang, D. Song, and C. Spanos, “Towards efficient data valuation based on the Shapley value,” _arXiv preprint arXiv:1902.10275_ , 2019. 

- [5] G. Wang, C. X. Dang, and Z. Zhou, “Measure contribution of participants in federated learning,” in _Proceedings of 2019 IEEE International Conference on Big Data (Big Data)_ . IEEE, 2019, pp. 2597–2604. 

- [6] J. Lin, M. Du, and J. Liu, “Free-riders in federated learning: Attacks and defenses,” _arXiv preprint arXiv:1911.12560_ , 2019. 

- [7] T. Luo, J. Huang, S. S. Kanhere, J. Zhang, and S. K. Das, “Improving IoT data quality in mobile crowd sensing: A cross validation approach,” _IEEE Internet of Things Journal_ , vol. 6, no. 3, pp. 5651–5664, Jun. 2019. 

- [8] X. Gong and N. Shroff, “Incentivizing truthful data quality for qualityaware mobile data crowdsourcing,” in _Proceedings of the 18th ACM International Symposium on Mobile Ad Hoc Networking and Computing_ , 2018, pp. 161–170. 

- [9] Y. Zhao, M. Li, L. Lai, N. Suda, D. Civin, and V. Chandra, “Federated learning with non-iid data,” _arXiv preprint arXiv:1806.00582_ , 2018. 

- [10] V. Shnayder, A. Agarwal, R. Frongillo, and D. C. Parkes, “Informed truthfulness in multi-task peer prediction,” in _Proceedings of the 2016 ACM Conference on Economics and Computation (EC)_ . ACM, 2016, pp. 179–196. 

- [11] N. Agarwal, A. T. Suresh, F. X. X. Yu, S. Kumar, and B. McMahan, “cpSGD: Communication-efficient and differentially-private distributed SGD,” in _Proceedings of the 2018 Advances in Neural Information Processing Systems (NIPS)_ , 2018, pp. 7564–7575. 

- [12] M. Abadi, A. Chu, I. Goodfellow, H. B. McMahan, I. Mironov, K. Talwar, and L. Zhang, “Deep learning with differential privacy,” in _Proceedings of the 2016 ACM SIGSAC Conference on Computer and Communications Security (CCS)_ , 2016, pp. 308–318. 

- [13] Z. Bu, J. Dong, Q. Long, and W. J. Su, “Deep learning with Gaussian differential privacy,” _arXiv preprint arXiv:1911.11607_ , 2019. 

- [14] G. Zhou, X. Zhu, C. Song, Y. Fan, H. Zhu, X. Ma, Y. Yan, J. Jin, H. Li, and K. Gai, “Deep interest network for click-through rate prediction,” in _Proceedings of the 24th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining (KDD)_ . ACM, 2018, pp. 1059– 1068. 

- [15] N. Miller, P. Resnick, and R. Zeckhauser, “Eliciting informative feedback: The peer-prediction method,” _Management Science_ , vol. 51, no. 9, pp. 1359–1373, 2005. 

- [16] E. Kamar and E. Horvitz, “Incentives for truthful reporting in crowdsourcing,” in _Proceedings of the 11th International Conference on Autonomous Agents and Multiagent Systems (AAMAS)_ . IFAAMAS, 2012, pp. 1329–1330. 

- [17] A. Dasgupta and A. Ghosh, “Crowdsourced judgement elicitation with endogenous proficiency,” in _Proceedings of the 22nd international conference on World Wide Web_ . ACM, 2013, pp. 319–330. 

- [18] A. Agarwal, D. Mandal, D. C. Parkes, and N. Shah, “Peer prediction with heterogeneous users,” in _Proceedings of the 2017 ACM Conference on Economics and Computation (EC)_ . ACM, 2017, pp. 81–98. 

- [19] C. Spearman, “The proof and measurement of association between two things.” 1961. 

- [20] F. J. Massey Jr, “The kolmogorov-smirnov test for goodness of fit,” _Journal of the American statistical Association_ , vol. 46, no. 253, pp. 68–78, 1951. 

- [21] S. W. Piche, “The selection of weight accuracies for Madalines,” _IEEE Transactions on Neural Networks_ , vol. 6, no. 2, pp. 432–445, 1995. 

- [22] H. Soula, G. Beslon, and O. Mazet, “Spontaneous dynamics of asymmetric random recurrent spiking neural networks,” _Neural Computation_ , vol. 18, no. 1, pp. 60–79, 2006. 

- [23] S.-S. Yang, C.-L. Ho, and S. Siu, “Computing and analyzing the sensitivity of MLP due to the errors of the iid inputs and weights based on CLT,” _IEEE Transactions on Neural Networks_ , vol. 21, no. 12, pp. 1882–1891, 2010. 

- [24] D. Yin, Y. Chen, K. Ramchandran, and P. Bartlett, “Byzantine-robust distributed learning: Towards optimal statistical rates,” _arXiv preprint arXiv:1803.01498_ , 2018. 

- [25] Y. Chen, L. Su, and J. Xu, “Distributed statistical machine learning in adversarial settings: Byzantine gradient descent,” _ACM SIGMETRICS Performance Evaluation Review_ , vol. 46, no. 1, pp. 96–96, 2019. 

- [26] H. Yu, Z. Liu, Y. Liu, T. Chen, M. Cong, X. Weng, D. Niyato, and Q. Yang, “A fairness-aware incentive scheme for federated learning,” in _Proceedings of the 2020 AAAI/ACM Conference on AI, Ethics, and Society (AIES)_ , 2020, pp. 393–399. 

- [27] R. Zeng, S. Zhang, J. Wang, and X. Chu, “Fmore: An incentive scheme of multi-dimensional auction for federated learning in MEC,” _arXiv preprint arXiv:2002.09699_ , 2020. 

- [28] L. Mu˜noz-Gonz´alez, K. T. Co, and E. C. Lupu, “Byzantine-robust federated machine learning through adaptive model averaging,” _arXiv preprint arXiv:1909.05125_ , 2019. 

- [29] J. Koneˇcn`y, H. B. McMahan, F. X. Yu, P. Richt´arik, A. T. Suresh, and D. Bacon, “Federated learning: Strategies for improving communication efficiency,” _arXiv preprint arXiv:1610.05492_ , 2016. 

- [30] T. Yang, G. Andrew, H. Eichner, H. Sun, W. Li, N. Kong, D. Ramage, and F. Beaufays, “Applied federated learning: Improving Google keyboard query suggestions,” _arXiv preprint arXiv:1812.02903_ , 2018. 

- [31] A. Hard, K. Rao, R. Mathews, F. Beaufays, S. Augenstein, H. Eichner, C. Kiddon, and D. Ramage, “Federated learning for mobile keyboard prediction,” _arXiv preprint arXiv:1811.03604_ , 2018. 

- [32] N. Ding, Z. Fang, and J. Huang, “Incentive mechanism design for federated learning with multi-dimensional private information,” in _2020 18th International Symposium on Modeling and Optimization in Mobile, Ad Hoc, and Wireless Networks (WiOPT)_ . IEEE, 2020, pp. 1–8. 

- [33] J. Huang, R. Talbi, Z. Zhao, S. Boucchenak, L. Y. Chen, and S. Roos, “An exploratory analysis on users’ contributions in federated learning,” _arXiv preprint arXiv:2011.06830_ , 2020. 

- [34] J. Kang, Z. Xiong, D. Niyato, S. Xie, and J. Zhang, “Incentive mechanism for reliable federated learning: A joint optimization approach to combining reputation and contract theory,” _IEEE Internet of Things Journal_ , vol. 6, no. 6, pp. 10 700–10 714, 2019. 

- [35] Y. Liu and J. Wei, “Incentives for federated learning: a hypothesis elicitation approach,” _arXiv preprint arXiv:2007.10596_ , 2020. 

- [36] J. Weng, J. Weng, H. Huang, C. Cai, and C. Wang, “Fedserving: A federated prediction serving framework based on incentive mechanism,” _arXiv preprint arXiv:2012.10566_ , 2020. 

