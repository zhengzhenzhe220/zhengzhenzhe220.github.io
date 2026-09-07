---
source: TMC23.pdf
pages: 17
converter: pymupdf4llm
converted_at: 2026-08-30T22:10:37+08:00
---

This article has been accepted for publication in IEEE Transactions on Mobile Computing. This is the author's version which has not been fully edited and content may change prior to final publication. Citation information: DOI 10.1109/TMC.2023.3316145 

IEEE TRANSACTION ON MOBILE COMPUTING, VOL. XXX, NO. XXX, XXX 

1 

# VAP: Online Data Valuation and Pricing for Machine Learning Models in Mobile Health 

Anran Xu, Zhenzhe Zheng, _Member, IEEE,_ Qinya Li, Fan Wu, _Member, IEEE,_ and Guihai Chen, _Fellow, IEEE_ 

**Abstract** —Mobile health (mHealth) applications, benefiting from mobile computing, have generated numerous mHealth data. However, they are dispersed across isolated devices, which hinders discovering insights underlying the aggregated data. Considering the online characteristics of mHealth, in this work, we present the first online data VAluation and Pricing mechanism, namely VAP, to incentive users to contribute mHealth data for machine learning (ML) tasks in mHealth systems. Under the Bayesian framework, we propose a new metric based on the concept of entropy to calculate data valuation during model training in an online manner. In proportion to the data valuation, we then determine payments as compensations for users to contribute their data. We formulate this pricing problem as a contextual multi-armed bandit with the goal of profit maximization and propose a new algorithm based on the characteristics of pricing. Furthermore, to tackle the budget constraint, we incorporate a two-stage multi-armed bandit with a knapsack method. We also extend VAP to advanced ML models by computing the entropy on the prediction space. Finally, we have evaluated VAP on two real-world mHealth data sets. Evaluation results show that VAP outperforms the state-of-the-art data valuation and pricing mechanisms in terms of computational complexity and extracted profit. 

**Index Terms** —Data Valuation, Online Pricing, Mobile Health 

✦ 

## **1 Introduction** 

M toring for health status, facilitate rapid diagnosis of poten-obile health (mHealth) technologies offer real-time moni- 

toring for health status, facilitate rapid diagnosis of poten-obile health (mHealth) technologies offer real-time monitial health issues, and provide remote healthcare services [1]. The recent developments towards intelligent mHealth systems, such as Apple Health [2], Google Fit [3], and Microsoft Health [4] are pieces of evidence of these trends [5]. Various machine learning (ML) models have been developed to extract information underlying mHealth data [5], [6], [7]. However, the obstacle to the wide adoption of ML in mHealth applications comes from _model uncertainty_ [8], which would provide unreliable prediction and is unacceptable in health applications [9]. The uncertainty of the model parameters often comes from insufficient training data and can be eliminated by acquiring enough data [8]. In mHealth, reducing the model uncertainty and accurately predicting a phenotype depends upon using a large amount of data from many other individuals with similar or related diseases. One potential approach to eliminate this dilemma is to collect extensive mHealth data from users as training data, harnessing the wisdom of crowd [10]. Thus, the further development of mHealth should have the ability to incentive users of mHealth services to contribute their data into the system to support ML models’ training. 

The valuable mHealth data are dispersed across isolated devices and have not been exploited efficiently. Users are reluctant to voluntarily share their personal health data due to the potential incurred costs and privacy concerns [11]. Health information privacy is the right of individuals to control the access, use, or disclosure of their identifiable health data [12]. And people’s agreement to share their data usually revolves around the value, which refers to the benefit that is accrued 

> _• A. Xu, Z. Zheng, Q. Li, F. Wu, and G. Chen are with the Department of Computer Science and Engineering, Shanghai Key Laboratory of Scalable Computing and Systems, Shanghai Jiao Tong University, China. (E-mail: {xuanran,zhengzhenzhe,qinyali}@sjtu.edu.cn, {fwu,gchen}@cs.sjtu.edu.cn)._ 

to the user or society due to the use of data [10]. Therefore, it is highly necessary to design an incentive mechanism to stimulate users to contribute their mHealth data. For incentive mechanism design in mHealth, we need to take the online characteristics of the data acquisition into account. First, the sensing data collected by mHealth can be obtained remotely in a streaming manner, which is often used for real-time predictive modeling [13]. Second, within the changing mHealth contexts, traditional static mHealth models may fail to respond with a correct prediction result. For example, people may carry out the same activity in a different manner or suffer from the same disease with various clinical symptoms [14]. Furthermore, population demographics, the prevalence of disease, and clinical practice may also evolve over time. This implies that predictions based on static data and models can become outdated and hence no longer be accurate [15]. Last, the users’ participation in the data acquisition process is dynamic. For example, in disease detection, the symptoms appear at an unpredictable time. To address these dynamics, many variants of online learning and incremental learning models are proposed [14], [15], [16], [17]. With these methods, the mHealth models could update over time as new data is collected and adapt quickly to new contexts. Besides, compared to the method that works with the sample pool once and for all, an online manner will not increase the permutation complexity. 

There are two critical components in designing an incentive mechanism: _data valuation and data pricing_ . The data valuation scheme quantifies the contribution of data within the context of ML model training. Based on this data valuation metric, the data pricing mechanism determines the compensation to users for their contributed data. We next summarize two major challenges for data valuation and pricing arising from the online characteristics of the data acquisition process in mHealth. 

The first challenge is to evaluate the contribution of newly arrived data in ML model training. The traditional data valuation schemes [18], [19], [20], [21], [22], built upon the concept 

Authorized licensed use limited to: Shanghai Jiaotong University. Downloaded on October 18,2023 at 01:05:52 UTC from IEEE Xplore.  Restrictions apply. © 2023 IEEE. Personal use is permitted, but republication/redistribution requires IEEE permission.��See https://www.ieee.org/publications/rights/index.html for more information. 

This article has been accepted for publication in IEEE Transactions on Mobile Computing. This is the author's version which has not been fully edited and 

content may change prior to final publication. Citation information: DOI 10.1109/TMC.2023.3316145 

2 

#### IEEE TRANSACTION ON MOBILE COMPUTING, VOL. XXX, NO. XXX, XXX 

of Shapley value from cooperative game theory [23], are not suitable for such an online learning situation. In these methods, all the data are collected in advance for model training, and the data contribution is evaluated at the end of model training. In contrast, we need to measure the data valuation in an online manner, based on the currently collected data, instead of the complete training data set. However, it is difficult to infer the data valuation at the intermediate model training without the global knowledge of the whole data set. Moreover, considering the privacy concerns in mHealth, compared to submitting whole data, it is more proper that users only upload part of the data (such as the feature of the data sample but not the label of it) to evaluate the data and query the price. Therefore, the data valuation module should have the ability to estimate the data contribution based on such kind of incomplete data. 

The second challenge is on designing profit-maximizing data pricing mechanisms within an asymmetric information environment. Some auction-based mechanisms have been proposed for data pricing [18], [24], [25]. However, the bidding model in the auction is unnecessarily complicated for data pricing, as users may often be reluctant to provide the minimum willing payment for their data or even do not know the exact value of this information. To this end, we turn to the posted pricing mechanism [26], where the service provider posts a public price, and the users only need to determine whether to accept the price and contribute the data. Nevertheless, the posted pricing mechanism introduces a heavy burden on the service provider. There is an information asymmetry over the minimum payment to data between the users and the service provider. Furthermore, users’ arrival sequences are also unknown to the service provider. Without complete information about the payment to data, it is hard for the service provider to set an appropriate price. The optimization of profit maximization needs to take both the revenue extracted from data valuation and the expenditure for data acquisition into account. In addition, there may be budget constraints in the system, maximizing the profit within a limited budget inevitably doubles the difficulty in the design of data pricing mechanisms. 

In this work, jointly considering the above challenges, we propose the first online data valuation and pricing mechanism for ML tasks in mHealth, namely VAP. We summarize our contributions as follows. 

_•_ Firstly, we introduce a novel metric for data valuation under the Bayesian perspective for Bayesian linear regression. This metric gauges the influence of data on the machine learning model training procedure. It is quantified by evaluating the entropy of the distributions over model parameters, permitting us to appraise data value in an online manner, eradicating the necessity for complete dataset collection. Furthermore, we enhance this data valuation metric from Bayesian linear regression to more intricate machine learning models by transitioning entropy computation from the parameter space to the prediction space. 

_•_ Secondly, we present an online data pricing mechanism that incorporates both data valuation and users’ reserve values. We formulate the determination of payments as a contextual multiarmed bandit (MAB) problem, aiming to maximize profit and propose a novel method for data pricing within this framework. Additionally, when facing the challenge of budget constraints in more complex scenarios, we model it as a two-stage multiarmed bandit problem with a knapsack and devise a solution. In both cases, a dual process of exploration and exploitation 


![](assets/TMC23/TMC23.pdf-0002-09.png)



![](assets/TMC23/TMC23.pdf-0002-10.png)



![](assets/TMC23/TMC23.pdf-0002-11.png)


<!-- Start of picture text -->
Online Learning<br>Data Valuation<br>1 mHealth data<br>2 posted price Data Pricing<br>3 submit data Update<br>4 payment<br>Data Contributors The Service Provider<br><!-- End of picture text -->

Fig. 1. Data acquisition process in a mHealth system. 

is employed to pinpoint optimal data prices, informed by user responses across diverse price points. Appreciating the inherent monotonicity of pricing, we exploit an expanded user feedback base, thereby securing a more profitable endeavor. 

_•_ Finally, we assess VAP’s performance utilizing two authentic mHealth datasets. The assessment results underline that our VAP holds supremacy over contemporaneous data valuation and pricing mechanisms for online Machine Learning tasks within mHealth frameworks, in terms of computational complexity and profit extraction. 

A preliminary version of this work [27] was published in INFOCOM 2022, which only proposed an individual pricing method without a theoretical guarantee. In this work, we add necessary proofs and property comparisons with traditional methods for data valuation. As for online data pricing, we add the regret analysis of VAP-Pricing and substantially extend the data pricing problem to a new situation under a fixed limited budget, and propose a new algorithm, namely VAP-PricingwK. We also add some experiments to validate the newly proposed method. 

The structure of this paper unfolds as follows: In Section 2, we present the system model and problem formulation. Subsequently, in Section 3, we propose an online data valuation metric based on the concept of entropy and delve into some of its characteristics. Moving forward, Section 4 is dedicated to the design of two distinct data pricing algorithms - one framed within the contextual Multi-Armed Bandit (MAB) schema, and the other following the Bandit with a Knapsack method, subject to a budget constraint. While in Section 5 we elaborate on incorporating VAP with more articulated machine learning models. The results of our performance evaluations take the stand in Section 6, followed by a review of related works in Section 7. Finally, we articulate the conclusion of our study in Section 8. 

## **2 Preliminaries** 

We consider the data acquisition process for a mHealth system in an adaptive way, as shown in Fig. 1. There are two types of participants involved in a mHealth system: data contributors and a service provider. The service provider trains online ML models on the collected data from data contributors to provide healthcare services. Due to the limited amount of data and the fading freshness of historical data, the ML models’ performance would decay over time. The service provider needs to acquire new mHealth data periodically to retrain the ML models. A specific data acquisition process is conducted as follows. At the time slot _t_ , first, a data contributor arrives and queries the price of her data by submitting the training data **_x_** without the label _y_ , 

Authorized licensed use limited to: Shanghai Jiaotong University. Downloaded on October 18,2023 at 01:05:52 UTC from IEEE Xplore.  Restrictions apply. © 2023 IEEE. Personal use is permitted, but republication/redistribution requires IEEE permission.��See https://www.ieee.org/publications/rights/index.html for more information. 

This article has been accepted for publication in IEEE Transactions on Mobile Computing. This is the author's version which has not been fully edited and content may change prior to final publication. Citation information: DOI 10.1109/TMC.2023.3316145 

IEEE TRANSACTION ON MOBILE COMPUTING, VOL. XXX, NO. XXX, XXX 

3 

where the feature **_x_** would help the service provider to evaluate the data valuation, and not releasing the label _y_ would preserve the content of data before the data exchange. Second, the service provider evaluates the data based on its contribution to ML model training, calculated by the performance improvement between the current model and the updated model after the data is added. Based on the _data valuation_ , the service provider posts the price determined by the _data pricing mechanism_ to the data contributor as incentives. Third, if the data contributor is satisfied with the price, she would contribute the complete training data ( **_x_** _, y_ ). Otherwise, she has no incentives to do so. Having received the data from multiple data contributors, the service provider would update the ML model, data valuation metric, and data pricing mechanism. Finally, the service provider gives the corresponding payment to the data contributor. We need to design an appropriate data valuation metric and a data pricing mechanism to quantify the performance improvement for model training and make a trade-off between the performance and data acquisition expenditure. 

We present a system model to describe the above data acquisition process. Each data contributor owns a set of private mHealth training data, each of which is a pair of a feature and the corresponding label, denoted by _d_ = ( **_x_** _, y_ ). We use _G_ **_X_** ( **_x_** ) to denote the contribution of a new data sample _d_ = ( **_x_** _, y_ ) to the model training. We consider each data contributor has a _reserve value v_ to her data set, which indicates the minimum unit willing price the data contributor would like to share her data. Similar to the previous work [24], [28], all data contributors’ reserve values follow an independent and identical distribution with probability density function _f_ ( _v_ ) over the range [0 _,_ 1]. Different from the classical Bayesian mechanism design [29], the probability density function is unknown to the service provider and needs to be learned from the interaction with data contributors. When one data contributor arrives at the online mHealth system, the service provider posts a unit price of _p_ for purchasing each piece of data. If the data contributor accepts the offered price ( _i.e. p ≥ v_ ), she would upload her data and get the corresponding payment; otherwise (0 _≤ p < v_ ), she would leave without contributing her data. The goal of the data pricing mechanism is to determine the posted price _p_ at each time slot to maximize the total profit, which will be defined in Section 4 later. 

## **3 Data Valuation** 

### **3.1 A Simple Case: Bayesian Linear Regression** 

To illustrate the idea of data valuation, we first consider a basic model in ML, linear regression [30] under the Bayesian framework. In mHealth, linear regression models are widely used in heart rate monitoring [17], blood pressure monitoring [31], mental illness detection [32], etc. More specifically, we use the ridge regression model as an example in this subsection and extend the concept of data valuation to more complex models such as Gaussian process (GP) [33] and Bayesian neural networks [34] later. 

Ridge regression can be explained under a Bayesian framework as a type of Bayesian linear regression [35], in which maximizing the parameter’s posterior probability by the Bayesian formula is the same as minimizing the loss function in the traditional frequentist view. Without loss of generality, we assume the prior probability of the parameters in ridge regression satisfy Gaussian distribution, _i.e. P_ ( **_β_** ) _∼N_ �0 _, ℓ_ 2I� with precision 

parameter (variance) _ℓ_<sup>2</sup> . The training process of ridge regression is to use new data to obtain posterior parameter distribution. Thus, the Bayesian framework provides a new perspective to interpret the model training process: the change of posterior parameter distribution can represent the evolution of the model training process to some extent. To calculate this change, we first express the posterior probability of the model parameter **_β_** from the Bayesian theorem: 


![](assets/TMC23/TMC23.pdf-0003-10.png)


where **_Y_** is the corresponding label of the data set ( **_X_** _,_ **_Y_** ), and _P_ ( **_Y_** _|_ **_β_** ) is the generation probability of **_Y_** under the model parameter **_β_** , and follows the Gaussian distribution. As the product of two Gaussian distributions _P_ ( **_Y_** _|_ **_β_** ) _P_ ( **_β_** ) is still Gaussian, the posterior parameter distribution _P_ ( **_β_** _|_ **_Y_** ) follows a Gaussian distribution. We denote the corresponding mean as **_β_ ¯** , and the variance as Σ. In this posterior Gaussian distribution, the exponential power should be equal. So that 


![](assets/TMC23/TMC23.pdf-0003-12.png)


Deriving from Equation (2), by equal coefficients of the same order, we can get: 


![](assets/TMC23/TMC23.pdf-0003-14.png)


Thus, _P_ ( **_β_** _|_ **_Y_** ) follows a Gaussian distribution with the mean and the variance of **_β_**<sup>**¯**</sup> = � **_X_**<sup>_⊤_</sup> **_X_** + _γ_<sup>_<u>ℓ</u>_22</sup><sup>**I**</sup> � _−_ 1 **_X_**<sup>_⊤_</sup> **_Y_** and Σ = � _γ_ <u>1</u><sup>2</sup><sup>**_X_**</sup><sup>_⊤_</sup><sup>**_X_**+</sup> _ℓ_<sup><u>12</u></sup><sup>**I**</sup> � _−_ 1, respectively. 

We regard the data’s contribution as how much information the data samples provide to the model training process. We use the metric of differential entropy [36], a concept from information theory, to measure the information contained underlying the corresponding model. When a new data sample is added to the training set, the parameter distribution shrinks, implying the reduction of the model parameters’ uncertainty. We quantify this uncertainty reduction as the differential entropy of the prior parameter distribution and the posterior parameter distribution. We further use the extent of this reduction to measure the contribution of a data sample to the model training. The differential entropy of the model parameter distribution (a Gaussian distribution) is defined as: 


![](assets/TMC23/TMC23.pdf-0003-17.png)


which is only related to variance Σ of the current distribution. And for the parameters **_β_** of one model, the parameter distribution depends on the collected training data. Thus, we denote the differential entropy of parameter distribution _H_ ( **_β_** _|_ **_Y_** ) on the data set ( **_X_** _,_ **_Y_** ) as _H_ ( **_X_** ), then the differential entropy of 

Authorized licensed use limited to: Shanghai Jiaotong University. Downloaded on October 18,2023 at 01:05:52 UTC from IEEE Xplore.  Restrictions apply. © 2023 IEEE. Personal use is permitted, but republication/redistribution requires IEEE permission.��See https://www.ieee.org/publications/rights/index.html for more information. 

This article has been accepted for publication in IEEE Transactions on Mobile Computing. This is the author's version which has not been fully edited and content may change prior to final publication. Citation information: DOI 10.1109/TMC.2023.3316145 

4 

IEEE TRANSACTION ON MOBILE COMPUTING, VOL. XXX, NO. XXX, XXX 

parameter distribution with the training data set ( **_X_** _,_ **_Y_** ) can be calculated by: 


![](assets/TMC23/TMC23.pdf-0004-04.png)


After adding new data sample ( **_x_** _, y_ ), the differential entropy of the parameter distribution is updated to 


![](assets/TMC23/TMC23.pdf-0004-06.png)


The posterior entropy reduction of the model parameter distribution is 


![](assets/TMC23/TMC23.pdf-0004-08.png)


**Definition 1.** _VAP-Valuation: The data valuation of data sample_ ( **_x_** _, y_ ) _for the model with data set_ ( **_X_** _,_ **_Y_** ) _is measured by G_ **_X_** ( **_x_** ) = 2<sup><u>1</u>ln</sup> �1 + **_x_** _⊤_ Σ **_Xx_** � _._ 

Thus, we can use _G_ **_X_** ( **_x_** ) to calculate the valuation of data **_x_** , by measuring the marginal contribution that the data **_x_** will make to the model that already has been trained by the data **_X_** . 

Considering the importance of reducing uncertainty in mHealth, we emphasize the relationship between _G_ **_X_** ( **_x_** ) and traditional predictive uncertainty. In Bayesian linear regression, in prediction space, for a new set of features **_x_** to be predicted, the predictive distribution takes the form _P_ ( _y|_ **_x_** _,_ **_β_** ) = _N_ � **_x_** _|_ **_β_** _⊤_ **_x_** _, σN_ 2<sup>(</sup><sup>**_x_**)</sup> �. A classic conclusion is that the predictive uncertainty can be determined by the variance _σN_<sup>2(</sup><sup>**_x_**)ofthe</sup> predictive distribution, which is given by 


![](assets/TMC23/TMC23.pdf-0004-12.png)


The first term represents the inherent noise in the generation of data, whereas the second term can reflect the uncertainty associated with the parameter **_β_** . We can notice that the determinants of a and b are the same, _i.e._ , **_x_**<sup>_⊤_</sup> Σ _X_ **_x_** . We will discuss the comparison between them in detail in Section 5. This important discovery will play an important role in our later extension of VAP-Valuation to more advanced models. 

### **3.2 Properties of Data Valuation Metric** 

Compared with traditional data valuation methods in ML such as Shapley value [18], [19], [20], VAP-Valuation has the following characteristics: 

### **Submodularity:** 

**Definition 2.** _( [37]) Let_ Ω _be a finite ground set and f_ : 2<sup>Ω</sup> _→_ R _. Then f is submodular if for all S, T ⊆_ Ω _with S ⊆T and every x ∈_ Ω _\T ,_ 


![](assets/TMC23/TMC23.pdf-0004-18.png)


For any data sets _S, T s.t. S ⊆T_ we define the set _U_ = _T −S_ . We use **_U_** , **_T_** , **_S_** to denote the features of the data samples in the set of _U_ , _T_ and _S_ : 


![](assets/TMC23/TMC23.pdf-0004-20.png)


Thus, we can get _G_ **_S_** ( **_x_** ) _> G_ **_T_** ( **_x_** ), which means the data valuation metric _G_ **_X_** ( **_x_** ) we proposed is submodular. A more intuitive understanding is that the marginal contribution of the data diminishes with the size of the data training set, which means that for the same data sample, the earlier the data is submitted, the higher the contribution generated. 

**Additivity:** For a collection of data sets submitted by a data contributor within a certain period, the total valuation of all the data ( _i.e._ , the total entropy reduction of the model parameter distribution) is the sum of the individual valuation of each data set. It is independent of the internal order of the data sets. That is, the data valuation metric is a set function: Owning ( **_X_** _,_ **_Y_** ), for any new data set _S_ , using _G_ ( _S_ ) to denote the data valuation of data set _S_ , calculated by the features **_S_** of data in _S_ , it is a fixed value: 


![](assets/TMC23/TMC23.pdf-0004-23.png)


More specifically, _G_ ( _S_ ) =<sup>�</sup> _si∈S_<sup>_G_�</sup><sup>_i_</sup> _j_<sup>_−_</sup> =1<sup>1</sup><sup>**_s_**</sup><sup>_j_(</sup><sup>**_s_**</sup><sup>_i_)regardlessthe</sup> position of _si_ in _S_ , though the specific value of _G_<sup>�</sup> _ij−_ =11<sup>**_s_**</sup><sup>_j_(</sup><sup>**_s_**</sup><sup>_i_)</sup> changes under different order of data sets. Moreover, the valuation of the entire dataset _I_ is completely distributed among all data contributors, _i.e. G_ ( _I_ ) =<sup>�</sup> _i∈I_<sup>_G_(</sup><sup>_i_),whichiseasily</sup> derived by the additivity. 

**Fairness:** Two data samples that are identical in what they contribute to the model have the same valuation in an online manner. That is, for any data _s_ and _s_<sup>_′_</sup> are equivalent in the sense that _G_ ( _S ∪{s}_ ) = _G_ ( _S ∪{s_<sup>_′_</sup> _}_ ) _, ∀S ⊆I\{s, s_<sup>_′_</sup> _}_ , then _GS_ ( _si_ ) = _GS_ ( _sj_ ) _._ Meanwhile, data with zero marginal contribution to the model has zero valuation, _i.e._ , if _G_ ( _S∪{s}_ ) = _G_ ( _S_ ), then _GS_ ( **_S_** ) = 0. Actually, because the variance of parameter distribution is non-negative, if data has zero valuation, it means the variance is zero, and then the Gaussian function becomes a Dirac delta function, in which **_β_** only has one possible value. 

**Label Anonymity:** According to Definition 1, in VAPValuation, each data’s valuation can be calculated only depending on the data features **_x_** , without using data label _y_ , which can preserve the content of the data before data exchange. On the other hand, VAP-Valuation can infer the contribution of **_x_** in realtime when the data is submitted, without waiting until the end 

Authorized licensed use limited to: Shanghai Jiaotong University. Downloaded on October 18,2023 at 01:05:52 UTC from IEEE Xplore.  Restrictions apply. © 2023 IEEE. Personal use is permitted, but republication/redistribution requires IEEE permission.��See https://www.ieee.org/publications/rights/index.html for more information. 

This article has been accepted for publication in IEEE Transactions on Mobile Computing. This is the author's version which has not been fully edited and content may change prior to final publication. Citation information: DOI 10.1109/TMC.2023.3316145 

5 

IEEE TRANSACTION ON MOBILE COMPUTING, VOL. XXX, NO. XXX, XXX 

of model training, which provides the possibility for subsequent online data pricing. 

**Comparison With Shapley Value Valuation (SVV):** 1) SVV is not submodular, and due to its computational characteristic, whenever a new data sample is added, the SVV of all data samples will need to be recalculated. 2) SVV also has additivity. In addition to this, the sum of SVV of all data samples is equal to 1, which is not available in VAP-Valuation. 3)SVV is the only valuation method with strict fairness. While our method can satisfy online fairness according to the above. 4)SVV does not have label anonymity, and can only be calculated after the whole complete data samples are obtained. 

can be formulated as a contextual bandit problem [41]. To solve it, we first rewrite the profit function as: 


![](assets/TMC23/TMC23.pdf-0005-06.png)


At time slot _t_ , we define Π _t_ = ( _π_ ( _Gt_ ) _, nt_ )<sup>_⊤_</sup> as the features of the context, where _Gt_ denotes the total contribution of the arriving data set, and _nt_ is the number of data samples. Then the expected reward of arm _pi_ can be expressed as: 


![](assets/TMC23/TMC23.pdf-0005-08.png)


## **4 Data Pricing** 

### **4.1 Profit Maximization Mechanism** 

In this section, we present a posted pricing mechanism, VAPPricing, to maximize the service provider’s profit in an online manner. According to Definition 1, _G_ **_X_** ( **_x_** ) denotes the contribution that one piece of data **_x_** brings to the performance improvement of model training, from which the service provider can extract profit. As we have mentioned before, each data contributor has a reserve value of _v_ . Only if the payment is higher than the reserve value would she upload her data and get the corresponding payment; otherwise, she would leave without contributing her data. Therefore, the profit that the service provider can obtain from one data contributor with a reserve value _v_ is: 


![](assets/TMC23/TMC23.pdf-0005-12.png)


where _p_ is the unit price of each data and _π_ ( _G_ **_X_** ( **_x_** )) is the revenue extracted from the updated model after adding _n_ data samples **_x_** . We use _F_ ( _p_ ) = �0 _p_<sup>_f_(</sup><sup>_v_)</sup><sup>_dv_to denote the probability</sup> that a data contributor accepts the data price _p_ . Thus, given the distribution of the reserve value _v_ and the price _p_ , the expected profit extracted from _n_ data samples can be written as: 


![](assets/TMC23/TMC23.pdf-0005-14.png)


As we do not know the distribution of reserve value, we tackle the above profit optimization problem by leveraging the exploration and exploitation technique from bandit literature [38], in which a decision-maker (the service provider) takes actions to maximize his long-term rewards (profits), by balancing between exploration and exploitation. At each time slot _t ∈{_ 1 _,_ 2 _, · · · , T }_ , a new data contributor with a value _vt_ arrives. The service provider chooses a posted price from the set of candidate prices _P_ ≜ � _pi | pi_ = _Ki_<sup>_, i_= 1</sup><sup>_, · · ·, K_</sup> �, where we regard each price _pi ∈ P_ as an arm as the traditional setting [39]. Then he observes the feedback from the data contributor and gets the corresponding profit according to Equation (12). 

The classical method UCB1 algorithm [40] estimates the unknown expected reward (profit) of each arm by making a linear combination of previously observed rewards of the arm. However, in our problem, the reward distribution behind each candidate price (arm) is not fixed, which is also determined by the valuation of data provided by the data contributor. Thus, we cannot directly use UCB1 to solve the online pricing problem. We observe that we can regard the data valuation as a type of context associated with each arm, and thus the pricing problem 

where _ωi_<sup>_∗_≜(</sup><sup>_Fv_(</sup><sup>_pi_)</sup><sup>_, −piFv_(</sup><sup>_pi_))</sup><sup>_⊤_representstheunknown</sup> coefficient vector. To post a reasonable price, that is, to select the best arm of each round, the service provider needs to estimate the expected rewards in Equation (15) of arms accurately. The service provider can obtain the value of Π _t_ based on the VAPValuation. Then we should learn _ωi_ of each arm, which can be explained as learning the reserve value distributions of data contributors implicitly. In this way, we can regard the features of the context as independent variables, and the expected reward is the dependent variable. With this, we can treat the observed context-reward pairs as training samples and train a regression model for each arm. 

However, different from the traditional setting in the LinUCB [41] to solve the contextual MAB problem, in our problem, the feedback information from each choice of one arm ( _i.e._ one possible posted price) can not only update the current arm but also be used as training inputs for other arms. That is when one data contributor rejects a specific price _pi_ , which means 0 _≤ pi < v_ , she would also reject the price _p_ with _p < pi_ . Similarly, when one data contributor accepts the price _pi_ , which means _pi ≥ v_ , she would also accept the price _p_ with _p > pi_ . Thus, in this work, we define _Mi_ as a design matrix of dimension _ji_<sup>_∗×_2 at time slot</sup><sup>_t_, whose rows correspond to</sup><sup>_j_</sup> _i_<sup>_∗_=</sup><sup>_ji_+</sup><sup>_jl_+</sup><sup>_js_</sup> training inputs, where _ji_ is the amount of training data with price _pi_ , _jl_ is the number of training data with _p > pi_ and the data contributor rejects the price _p_ , _js_ is the number of data with price _p < pi_ and the data contributor accepts the price _p_ . And _ci_ is the rewards corresponding to these contexts. With this augmented training data set ( _Mi, ci_ ), we can have a better estimate of the coefficients by applying ridge regression: 


![](assets/TMC23/TMC23.pdf-0005-19.png)


where _I_ is the 2 _×_ 2 identity matrix. 

Algorithm 1 gives a detailed description of the entire LinUCB algorithm for pricing, in which _Ai_ = _Mi_<sup>_⊤Mi_+</sup><sup>_I_and</sup><sup>_bi_=</sup> _Mi_<sup>_⊤ci_. For the input of the algorithm,</sup><sup>_α_is a parameter to control</sup> the exploration scale, _G_ **_X_** ( **_x_** ) is the VAP-Valuation of **_x_** , _π_ ( _·_ ) is the revenue function, _K_ is the number of arms (candidate price), and _T_ is the total time slots. At each time slot, there is a data contributor _t_ querying the price by her data **_x_** _t_ , and then we can observe the context (features of the current data) Π _t_ (Line 2). Then for all possible prices, we estimate the coefficients according to Equation (16) (Lines 3-6). It can be shown that with probability at least 1 _− δ_ : 


![](assets/TMC23/TMC23.pdf-0005-22.png)


Authorized licensed use limited to: Shanghai Jiaotong University. Downloaded on October 18,2023 at 01:05:52 UTC from IEEE Xplore.  Restrictions apply. © 2023 IEEE. Personal use is permitted, but republication/redistribution requires IEEE permission.��See https://www.ieee.org/publications/rights/index.html for more information. 

This article has been accepted for publication in IEEE Transactions on Mobile Computing. This is the author's version which has not been fully edited and content may change prior to final publication. Citation information: DOI 10.1109/TMC.2023.3316145 

IEEE TRANSACTION ON MOBILE COMPUTING, VOL. XXX, NO. XXX, XXX 

6 

|**Al**|**gorithm 1:**VAP-Pricing|
|---|---|
|**I**|**nput:**_α ∈_R<sup>+</sup>,_G_**_X_**(**_x_**),_π_(_·_),_K_,_T_|
|**1 f**|**or**_t_= 1_to T_ **do**|
|**2**|Observe the features of current data<br>|
||Π_t_ = (_π_(_G_**_X_**(**_x_**_t_))_, nt_)<sup>_⊤_</sup>;|
|**3**|**for**_i_= 1_to K_ **do**|
|**4**|**if** _pi is new_**then**|
|**5**|_Ai ←I_,_bi ←_**0**;|
|**6**|�_ωi ←A_<sup>_−_1</sup><br>_i _<sup>_bi_, �</sup><sup>_µi,t ←_Π</sup><sup>_⊤_</sup><br>_t_ <sup>�</sup><sup>_ωi_</sup> <sup>+</sup><sup>_α_</sup><br>�<br>Π<sup>_⊤_</sup><br>_t _<sup>_A−_1</sup><br>_i_ <sup>Π</sup><sup>_t_;</sup>|
|**7**|Choose the arm_It_ = argmax<br>_i_=1_,··· ,K_<br>_µi,t_;|
|**8**|**Posted price**_p_= min(_pIt, ⌊π_(_G_**_X_**(**_x_**_t_))_/n⌋_);|
|**9**|Observe and record the response from the data<br>contributor_t_;|
|**10**|**if** _t is satisfied with the price (pIt ≥vt)_ **then**|
|**11**|**for**_i_=_It to K_ **do**|
|**12**|_rt_ =_π_(_G_**_X_**(**_x_**_t_))_−ntpi_;|
|**13**|_Ai ←Ai_+ Π_t_Π<sup>_⊤_</sup><br>_t_ <sup>,</sup><sup>_bi_</sup> <sup>_←bi_</sup> <sup>+</sup><sup>_rt_Π</sup><sup>_t_;</sup>|
|**14**|**_X_** = **_X_** + **_x_**_t_;|
|**15**|**else**|
|**16**|**for**_i_= 1_to It_ **do**|
|**17**|_rt_ = 0;|
|**18**|_Ai ←Ai_+ Π_t_Π<sup>_⊤_</sup><br>_t_ <sup>,</sup><sup>_bi_</sup> <sup>_←bi_</sup> <sup>+</sup><sup>_rt_Π</sup><sup>_t_;</sup>|
|**19**|Update function_G_**_X_**(**_x_**);|



for any _δ >_ 0, where _αT_ = 1+ �2 ln<sup><u>1</u></sup> _δ_<sup>+ 2 ln</sup> <u>�1 +</u> 2 _<u>t</u>_ <u>�. We will</u> show this result in Section 4.3. The inequality gives a reasonably tight upper confidence bound for the expected reward of arm _pIt_ , from which a UCB-type arm-selection strategy can be derived: at each time slot _t_ , choose 


![](assets/TMC23/TMC23.pdf-0006-05.png)


The criterion for arm selection can also be regarded as an additive trade-off between the reward estimation and model uncertainty reduction (Lines 7-8). After we post a price, we record the response from the data contributor. If the data contributor accepts the posted price, _i.e._ , _pIt ≥ vt_ , we calculate the reward and update _Ai_ as well as _bi_ for all price _pi > pIt_ . The data contributor would upload her data, and we add it to the data set (Lines 10-14). Otherwise, _i.e._ , 0 _≤ pIt < vt_ , the data contributor would leave without contributing her data. The reward we get is 0, and we update _Ai_ as well as _bi_ for all price _pi < pIt_ (Lines 15-18). 

Next, we introduce the design of revenue function _π_ . By the additivity property of data valuation metric in Section 3.2, we can get _G_ ( _S ∪T_ ) = _G_ ( _S_ ) + _G_ ( _T_ ). To make the revenue function extend the additivity, _i.e. π_ ( _G_ ( _S ∪T_ )) = _π_ ( _G_ ( _S_ )) + _π_ ( _G_ ( _T_ )), it is easy to prove that _π_ ( _·_ ) should be the linear function by Cauchy’s functional equation [42] as 


![](assets/TMC23/TMC23.pdf-0006-08.png)


In this work, we set _π_ ( _G_ **_X_** ( **_x_** )) = _k · G_ **_X_** ( **_x_** ) _− ϵ_ , where _k_ can uniform the magnitude between the data valuation and the revenue. As we have mentioned, _k · G_ **_X_** ( **_x_** ) guaranteed the additivity when converting data valuation _G_ **_X_** ( **_x_** ) to _p_ . Besides, 

_ϵ_ can be seen as the fee per operation, which can also control the trade-off between total entropy reduction (data valuation) and the total budget, which we will show in the evaluation part. By setting proper _ϵ_ , the service provider can acquire data with different objectives. For example, a budget-limited service provider may have a limited budget who only wants to collect a smaller data set and can tolerate a slower data collection rate. On the other hand, a budget-sufficient service provider has more budget and wants to collect as much data as possible. A suitable _π_ ( _·_ ) can control the trade-off between the data collection scale and the total budget. 

### **4.2 Properties of Data Pricing Mechanism** 

The data pricing mechanism we proposed in VAP-Pricing has the following characteristics: 

**Incentive for Data Contribution:** VAP-Pricing motivates data contributors to submit data as early as possible because the data valuation function _G_ **_X_** ( **_x_** ) is submodular with respect to **_X_** . Specifically, in VAP-Pricing, earlier data contributors will have a higher (marginal) data contribution and are more likely to get more profit, implying that we encourage data contributors to submit data as soon as possible in the online data collection process. 

**Robust to Strategic Behaviors:** To guarantee the property of symmetry, Shapley value leaves the possibility for selfish data contributors to carry out strategic behaviors, such as copying data for extra benefits. There are some solutions to solve this issue, such as discounting the value of the same data [18], but it will break the property of fairness in Shapley value. However, VAP-Pricing can naturally decrease the similar data’s valuation, as the later data will not impact the model too much due to the submodularity of VAP-Valuation. Meanwhile, the data with the same contribution will be given the same price at one specific time slot. Thus, VAP-Pricing guarantees fairness to some extent. 

Moreover, this data pricing mechanism is also arbitrage-free when the VAP-Pricing is stable. Due to the additivity of VAPValuation, regardless of the data order in a data set, the sum of the data valuation for a dataset is the same, resulting in the identical posted price. Specifically, we consider the case when the pricing mechanism is stable, _i.e._ we have already got the accurate _Fv_ ( _p_ ). Suppose the data contributor divides a data set **_S_** into several subsets **_S_** _i_ , _i_ = 1 _, · · · , n_ , and submits each subset at different time slots. Then by the additivity property of VAP-Valuation and the definition of revenue function _π_ , we can further get 


![](assets/TMC23/TMC23.pdf-0006-16.png)


where we denote _G_ = _G_ **_X_** ( **_S_** ) for the whole data set and _Gi_ = _G_ **_X_ +**<sup>**�**</sup> **_ij−_ =11**<sup>**_S_**</sup> _S_<sup>**_j_**(</sup><sup>**_S_**</sup><sup>_i_)foreachsubset.Wedenote</sup><sup>_p_1</sup><sup>_,i_astheposted</sup> price for each separated data subset and _p_ 2 as the posted price for the whole data set. Then, 


![](assets/TMC23/TMC23.pdf-0006-18.png)


As _Fv_ ( _p_ ) is already known, it is easy to prove that _p_ 1 _,i_ = _p_ 2 _− ϵ_ = _v_ when _p ≥ v_ , which means if the full dataset can be 

Authorized licensed use limited to: Shanghai Jiaotong University. Downloaded on October 18,2023 at 01:05:52 UTC from IEEE Xplore.  Restrictions apply. © 2023 IEEE. Personal use is permitted, but republication/redistribution requires IEEE permission.��See https://www.ieee.org/publications/rights/index.html for more information. 

This article has been accepted for publication in IEEE Transactions on Mobile Computing. This is the author's version which has not been fully edited and content may change prior to final publication. Citation information: DOI 10.1109/TMC.2023.3316145 

7 

IEEE TRANSACTION ON MOBILE COMPUTING, VOL. XXX, NO. XXX, XXX 

traded, data contributors can not get more payment by splitting the data set and submitting them separately. Intuitively, if the data contributor splits the data and submits them separately due to the influence of the operation fee _ϵ_ in the mapping function, it results in a lower payment. 

**Data Privacy Preserving for mHealth:** By the Label Anonymity property of VAP-Valuation, the data contributor _i_ can query the possible payment by _xi_ without uploading _yi_ . Then the label _yi_ is not involved in the data valuation and pricing processes, reducing the risk of privacy leakage. Thus, in the data collection process, the data contributors have the right to decide whether the data is used for model training under the VAP-Pricing framework. Suppose the data contributors are not satisfied with the current payment and choose not to contribute their whole data. In this case, they do not leak the whole information about their data (preserve the label _y_ ). 

### **4.3 Regret Analysis** 

For stochastic linear bandits, a classic setting is a shared parameter with possibly infinite arms. In our problem, we follow the original version, considering fixed _K_ arms and disjoint parameters, _i.e._ , the posted price set is fixed finite, and for each arm, coefficient vector _ωi_<sup>_∗_≜(</sup><sup>_Fv_(</sup><sup>_pi_)</sup><sup>_, −piFv_(</sup><sup>_pi_))</sup><sup>_⊤_.</sup> 

We define the regret of VAP-Pricing as: 


![](assets/TMC23/TMC23.pdf-0007-08.png)


where _i_<sup>_∗_</sup> is the optimal arm (price) and _it_ is the arm taken at time slot _t_ . The proof is divided into two steps, the first is that the regret of the shared-parameter setting will be _O_ ( _√dT_ ). In this setting, there is only a fixed unknown parameter _ω_<sup>_∗_</sup> for all arms, where _ω_<sup>_∗_</sup> _∈_ R<sup>_d_</sup> . After that, we show the regret of the disjoint-parameter setting under our problem setting will reach _O_ ( _√dKT_ ). Considering the shared-parameter setting, first, we make some assumptions, which are common in the traditional stochastic linear bandits problem. 

**Assumption 1.** _We assume that the observed noise i.e., (rt −_ Π<sup>_⊤_</sup> _t_<sup>_ω∗)isindependentstandardGaussiannoise,wherertisthe_</sup> _reward and ω_<sup>_∗_</sup> _∈_ R<sup>_d_</sup> _is an unknown but fix parameter._ 

**Assumption 2.** _We assume that the contexts_ Π _and the parameter ω_<sup>_∗_</sup> _are bounded. ∥_ Π _∥_ 2 _≤_ 1 _, ∥ω_<sup>_∗_</sup> _∥_ 2 _≤_ 1 _._ 

Then the regret under the shared-parameter setting is: 


![](assets/TMC23/TMC23.pdf-0007-13.png)


where Π _∗_ is the optimal action and Π _t_ is the action taken at time slot _t_ . To note, it is different from the previous definition of Π. Here we reuse the symbol for simplicity. The actions here contain both the original context and the information of the arm selection, which will be introduced in detail in Equation (34) later. To complete the proof, we introduce the concept of confidence ellipsoid. The result shows that _ω_<sup>_∗_</sup> lies with high probability in an ellipsoid with center _ω_ � [43]. 


![](assets/TMC23/TMC23.pdf-0007-15.png)


Then we can get the regret of shared-parameter LinUCB. **Theorem 1.** _With probability_ 1 _− δ, the regret RT of sharedparameter LinUCB satisfies_ 


![](assets/TMC23/TMC23.pdf-0007-17.png)


= _where T is the total time slots, the hyperparameter αT √λ_ + �2 ln<sup><u>1</u></sup> _δ_<sup>+</sup><sup>_d_ln</sup> <u>�1 +</u> _dλt_ <u>�</u> _, d is dimension the unknown parameters, and λ is the coefficient of the identity matrix in the gram matrix._ 

_Proof._ By Cauchy-Schwarz and Lemma 1, we have 


![](assets/TMC23/TMC23.pdf-0007-20.png)


Let _ω_ � _t ∈ Ct_ be the parameter in the confidence set to make that _ω_ � _t_<sup>_⊤_Π</sup><sup>_t_= max</sup><sup>_ω∈C_</sup> _t_<sup>_ω⊤_Π Thus,</sup> 


![](assets/TMC23/TMC23.pdf-0007-22.png)


As the definition of _αT_ , we can get _αT ≥_ 1. By the Assumption 3, we have _Rt ≤_ 2 _αT_ min _{_ 1 _, ∥_ Π _it∥A−t−_ 11<sup>_}_. Then by the Cauchy-</sup> Schwarz inequality and min _{_ 1 _, x} ≤_ 2 ln(1 + _x_ ), we can bound the regret as 


![](assets/TMC23/TMC23.pdf-0007-24.png)


By the definition of _A_ , we have 


![](assets/TMC23/TMC23.pdf-0007-26.png)


Authorized licensed use limited to: Shanghai Jiaotong University. Downloaded on October 18,2023 at 01:05:52 UTC from IEEE Xplore.  Restrictions apply. © 2023 IEEE. Personal use is permitted, but republication/redistribution requires IEEE permission.��See https://www.ieee.org/publications/rights/index.html for more information. 

This article has been accepted for publication in IEEE Transactions on Mobile Computing. This is the author's version which has not been fully edited and content may change prior to final publication. Citation information: DOI 10.1109/TMC.2023.3316145 

8 

IEEE TRANSACTION ON MOBILE COMPUTING, VOL. XXX, NO. XXX, XXX 

Then, by AM-GM inequality, we can get 


![](assets/TMC23/TMC23.pdf-0008-04.png)


with det _A_ 0 = _λ_<sup>_d_</sup> , we can further get 


![](assets/TMC23/TMC23.pdf-0008-06.png)


Then, we can continue bounding the regret as 


![](assets/TMC23/TMC23.pdf-0008-08.png)


Till now, we obtain the regret of the shared-parameter setting with a single true _ω_<sup>_∗_</sup> assumed. 

**Theorem 2.** _With probability_ 1 _− δ, the regret of disjointparameter VAP-Pricing satisfies_ 


![](assets/TMC23/TMC23.pdf-0008-11.png)


_where T is the total time slots, K is the number of arms, and αT_ = _√λ_ + �2 ln<sup><u>1</u></sup> _δ_<sup>+</sup><sup>_d_ln</sup> <u>�1 +</u> _dλt_ <u>�</u> _in VAP-Pricing._ 

An intuitive understanding is that the regret of VAP-Pricing is related to the number of arms (prices) set _K_ and the total time slots _T_ . As a bigger arm size, the regret will increase due to a larger range of policies, and VAP-Pricing can get logarithmic accumulated regret. Also, as _α_ is related to _δ_ , the choice of _α_ in VAP-Pricing will affect the probability of the regret guarantee. 

_Proof._ In our problem, the parameter is disjoint over each arm so we have _K_ separate parameters _ωi_<sup>_∗_to estimate, one for each arm.</sup> Then it is obvious the regret of the disjoint-parameter situation is a factor of _K_ worse than that of the shared-parameter LinUCB. Another explanation for this is that we can generate a new parameter Ω<sup>_∗_</sup> , to make 


![](assets/TMC23/TMC23.pdf-0008-15.png)


where _ωi_<sup>_∗∈_R</sup><sup>_d_.ThusbythedefinitionofΩ</sup><sup>_∗_,wehaveΩ</sup><sup>_∗∈_</sup> R<sup>_D_</sup> _, D_ = _dK_ . Then we can get under shared-parameter Ω<sup>_∗_</sup> , the regret is bounded by _O_ ( _D√T_ ) = _O_ ( _dK√T_ ). 

### **4.4 VAP-Pricing Under Fixed Limited Budget** 

In Section 4.1, we considered that the service provider’s budget is not fixed, and it can be adjusted by _ϵ_ . However, in this section, we consider another common situation in real-life situations, where the budget is fixed at the beginning. In this case, we cannot simply model it as an ordinary contextual multi-armed bandit problem as before. This is because we need to consider not only the revenue brought by the current arm each time we pull the arm but also the budget consumption at the same time to ensure that we can get the maximum revenue when the budget is depleted. Then a straightforward idea is to model it as a linear contextual bandit with backpacks problem, which is an extended version of VAP-Pricing above when considering fixed budgets. Linear contextual bandits with backpacks had been studied by previous work [44]. However, we can not apply the previous method to our model. In previous work, it was assumed that there is a fixed but unknown distribution _D_ on the context. Whereas in our modeling, contexts (Π _t_ = ( _π_ ( _Gt_ ) _, nt_ )<sup>_⊤_</sup> , _i.e._ , data valuation and the number of data samples) do not follow a fixed distribution (the data valuation is diminishing marginal). The good news is that the part not known to the data provider and needs to be inferred by the VAP-Pricing is the reserve value distribution _Fv_ ( _p_ ) of data providers. It is a deterministic distribution that does not vary over time. Thus, considering the budget limitation, we can remodel the problem to a static multi-armed bandit with a knapsack framework, instead of considering time-varying contexts (data valuations). In the first stage, we predict the reserve value distribution of the data contributors through a static multi-armed bandit, and then we combine the expected reserve value distribution and the current data valuation to compute the accurate posted price. 

Next, we give a formal definition of this problem. The service provider is given access to _d_ -dimensional of _K_ arms (price) denoted as _a ∈_ [ _K_ ] := _{_ 1 _,_ 2 _, . . . , K}_ . Each time _t ∈_ [ _T_ ], the service provider pulls an arm _at_ and observes the reward and consumption. We denote the unknown expected reward as _rt_ , and the corresponding resource consumption as _ct_ . We assume there is a fixed total budget _B ∈_ R+ on the consumption, And _B_ is a hard constraint on resource consumption. The algorithm stops at the earliest time _τ_ when _B_ is exhausted. 

To solve this bandit with knapsack problem, we decomposite the budget into each slot. For submission with _n_ pieces of data samples, we regard the strategy as the repeated _n_ posted price. Thus, in each time slot, we only need to consider the unit reward and the unit cost of each price _pi, i ∈_ [ _K_ ]. First, we define the unit reward (profit) and cost for each arm. The reward (profit) that the service provider can obtain from one data contributor with a reserve value _v_ is: 


![](assets/TMC23/TMC23.pdf-0008-21.png)


, where arm _i ∈_ [ _K_ ]. And the unit cost that the service provider pays for each arm _i_ with a reserve value _v_ is: 


![](assets/TMC23/TMC23.pdf-0008-23.png)


As we mentioned above, we transform them into functions related to _Fv_ ( _pi_ ), 


![](assets/TMC23/TMC23.pdf-0008-25.png)


Authorized licensed use limited to: Shanghai Jiaotong University. Downloaded on October 18,2023 at 01:05:52 UTC from IEEE Xplore.  Restrictions apply. © 2023 IEEE. Personal use is permitted, but republication/redistribution requires IEEE permission.��See https://www.ieee.org/publications/rights/index.html for more information. 

This article has been accepted for publication in IEEE Transactions on Mobile Computing. This is the author's version which has not been fully edited and 

content may change prior to final publication. Citation information: DOI 10.1109/TMC.2023.3316145 

IEEE TRANSACTION ON MOBILE COMPUTING, VOL. XXX, NO. XXX, XXX 

9 


![](assets/TMC23/TMC23.pdf-0009-04.png)


Then in first stage, we calculate the _Fv_ ( _pi_ ): 


![](assets/TMC23/TMC23.pdf-0009-06.png)


where _f_ ( _i_ ) is the number of times that data contributors accept _pi_ , _i.e._ , _pi ≥ v_ in _m_ ( _i_ ). Then based on the estimation of _Fv_ ( _pi_ ), we can calculate the expected reward and cost. We give detailed data pricing with a knapsack algorithm, called VAP-PricingwK in Algorithm 2. For the input of the algorithm, _α_ is a parameter to control the exploration scale, _K_ is the number of arms (candidate price), _T_ is the total time slots, _B_ is the total Budget of the service provider, _ϵ_ is the budget factor, _G_ **_X_** ( **_x_** ) is the VAP-Valuation of **_x_** , and _π_ ( _·_ ) is the revenue function. We initialize the parameter _f_ ( _i_ ) and _m_ ( _i_ ) for each arm _i_ (Lines 1-2), and for all possible prices, we pull each arm once (Lines 5-6). As for each time slot _t_ , there is a data contributor _t_ querying the price by her data **_x_** _t_ . First, we estimate the reserve value distribution as Equation (38) based on the historical observation (Line 9). To estimate the reward _rt_ ( _i_ ) and cost _ct_ ( _i_ ) for each arm, inspired by the UCB-based algorithm for BwK [45], which is based on “optimism in the face 

of uncertainty”, we make optimistic estimates of them: 


![](assets/TMC23/TMC23.pdf-0009-09.png)


where _r_ ˜ _t_ ( _i_ ) is the upper confidence bound of _rt_ ( _i_ ) and _c_ ˜ _t_ ( _i_ ) is the lower confidence bound of _ct_ ( _i_ ) (Lines 10-11). After getting _r_ ˜ _t_ ( _i_ ) and _c_ ˜ _t_ ( _i_ ), we solve the following linear programming to get the policy: 


![](assets/TMC23/TMC23.pdf-0009-11.png)


where **_q_** is the probability to pull each arm, and _ϵ_ = � _<u>γBd</u>_<sup>+</sup> log( _T_ )<sup>_<u>γ</u>_</sup> _B_<sup>_d, γ_=log</sup> � _<u>T dδ</u>_ �. Then we select arm _It_ randomly according to the probability in **_q_** , and post the price (Lines 1214). After posting a price, we record the response from the data contributor. If the data contributor accepts the posted price, _i.e._ , _p ≥ vt_ , we update _f_ ( _i_ ) as well as _m_ ( _i_ ) for all arms _i > It_ . The data contributor would upload her data, and we add it to the data set (Lines 15-21). Otherwise, _i.e._ , 0 _≤ p < vt_ , the data contributor would leave without contributing her data. We only update _m_ ( _i_ ) for all arms _i ≤ It_ (Lines 23-24). 

## **5 Extensions to General Models** 

In this section, we extend VAP to advanced ML models. In Bayesian linear regression, we can easily calculate the posterior parameter distribution by a closed-form expression. However, in other advanced ML models, such as Bayesian neural network [34], parameter spaces are often high dimensional, and computing their entropy is usually intractable. Furthermore, for nonparametric processes, such as the Gaussian process [33], the parameter space is infinite-dimensional, which further increases the computational complexity. 

To solve this problem, inspired by Equaition (9) and Equation (8), we transfer the objective from computing uncertainty in the parameter space to the prediction space, avoiding gridding parameter space (exponentially hard with dimensionality). Fig. 2 shows the comparison of parameter probability density distribution and prediction uncertainty. We can find that they have the same shrinking trend when adding more training data. The model’s grasp of the parameter is getting higher, implying the model uncertainty and prediction uncertainty reduction. Thus, the data valuation we obtained can be regarded as a measure of uncertainty. The difference is that Equation (9) calculates the predictive distribution variance in the prediction task, the aim of which is to get the uncertainty in the current test data to evaluate the reliability of a prediction. However, Equation (8) calculates the entropy reduction of parameter **_β_** caused by adding new training data from the training data set. The goal is to get the model uncertainty changes caused by current training data to measure each data’s contribution. 

Thus, we can calculate entropy in low-dimensional output space using the idea of prediction uncertainty. For new data, _d_ = ( **_x_** _, y_ ), we calculate its contribution by regarding **_x_** as the features of the prediction task to calculate its prediction uncertainty. Specifically, for a representative non-parametric model, we write Gaussian process regression(GPR) as **_y_** = _f_ ( **_x_** ) + **_ε_** 

Authorized licensed use limited to: Shanghai Jiaotong University. Downloaded on October 18,2023 at 01:05:52 UTC from IEEE Xplore.  Restrictions apply. 

© 2023 IEEE. Personal use is permitted, but republication/redistribution requires IEEE permission.��See https://www.ieee.org/publications/rights/index.html for more information. 

This article has been accepted for publication in IEEE Transactions on Mobile Computing. This is the author's version which has not been fully edited and content may change prior to final publication. Citation information: DOI 10.1109/TMC.2023.3316145 

IEEE TRANSACTION ON MOBILE COMPUTING, VOL. XXX, NO. XXX, XXX 

10 


![](assets/TMC23/TMC23.pdf-0010-03.png)


<!-- Start of picture text -->
6 6 6<br>5 5 5<br>4 4 4<br>3 P(β) 3 P(β) 3 P(β)<br>2 2 2<br>1 1 1<br>0 0 0<br>3 3 3<br>2 2 2<br>1 1 1<br>−3 −2 −1β10 1 2 3 −3−2−10 β2 0.0 0.5 1.0β11.5 2.0 2.5 3.0 −3−2−10 β2 0.0 0.5 1.0β11.5 2.0 2.5 3.0 −3−2−10 β2<br>(a) Change of parameter distribution. The amount of training data increases from left to right (2, 100, and 600). We only show two dimensions of<br>parameter  β 1 and  β 2 for straightforward demonstration.<br>1.2 prediction 1.0 prediction 1.0 prediction<br>1.0 training data 0.8 training data 0.8 training data<br>0.8<br>0.6 0.6<br>y 0.6 y y<br>0.4 0.4 0.4<br>0.2<br>0.2<br>0.0 0.2<br>−0.2 0.0 0.0<br>0.4 0.5 0.6 0.7 0.8 0.9 1.0 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0<br>x1 x1 x1<br><!-- End of picture text -->

(a) Change of parameter distribution. The amount of training data increases from left to right (2, 100, and 600). We only show two dimensions of parameter _β_ 1 and _β_ 2 for straightforward demonstration. 

(b) Change of prediction uncertainty. The amount of training data increases from left to right (2, 100, and 600). _x_ 1 is one of the features of training data, and _y_ is the corresponding label. The pink line is the prediction of the current model, and the blue shaded area is the corresponding prediction uncertainty. 

Fig. 2. Model Changes during data addition. 

with the unknown function _f_ follows a _N_ ( _µ, k_ ) and **_ε_** follows a _N_ (0 _, γ_<sup>2</sup> _I_ ) [33]. Different from parameter **_β_** in range regression, there are no specific parameters in _f_ . Thus, GPR is a non-parametric model. Consider the current purchased data set _D_ = _{di}_<sup>_n_</sup> _i_ =1<sup>containingndatawith</sup><sup>_di_=(</sup><sup>**_x_**</sup><sup>_i, yi_),</sup> [ _f_ ( **_x_** 1) _, f_ ( **_x_** 2) _, . . . , f_ ( **_x_** _n_ )]<sup>_⊤_</sup> _∼N_ ( **_µ_** _, K_ ), where **_µ_** is the mean vector and **_K_** is the _n × n_ covariance matrix, **_K_** _ij_ = _k_ ( **_x_** _i,_ **_x_** _j_ ). To make a prediction of new data sample **_x_** by the current model, the predictive distribution is: 

be measured. For classification, the model prediction can be approximated using Monte Carlo integration as follows: 


![](assets/TMC23/TMC23.pdf-0010-09.png)


with _T_ sampled masked model weights **_W_**<sup>�</sup> _t ∼ q_ **_θ_**<sup>_∗_(</sup><sup>**_W_**)</sup><sup>_,_where</sup> _q_ **_θ_**<sup>_∗_(</sup><sup>**_W_**) is the Dropout distribution [8]. Then the valuation func-</sup> tion can be calculated by: 


![](assets/TMC23/TMC23.pdf-0010-11.png)



![](assets/TMC23/TMC23.pdf-0010-12.png)


where the predictive distribution variance is: 

where _R_ is the number of categories. For regression, the predicΣ **_x_** = **_K_** ( **_x_** _,_ **_x_** ) tions are made by approximating the predictive mean: 


![](assets/TMC23/TMC23.pdf-0010-15.png)



![](assets/TMC23/TMC23.pdf-0010-16.png)


Then, similar to the Equation (8), the valuation function in GPR can be set as 

The prediction uncertainty is captured by the predictive variance, which can be approximated as: 


![](assets/TMC23/TMC23.pdf-0010-19.png)



![](assets/TMC23/TMC23.pdf-0010-20.png)


Moreover, for the complex parametric model, neural network, similar to the Bayesian linear regression, we can put a prior distribution over its weights, such as a Gaussian prior distribution: **_W_** _∼N_ (0 _, γ_<sup>2</sup> _I_ ). Such a model is referred to as a Bayesian neural network (BNN) [34]. For each new data _x_ , we can obtain the corresponding predictive distribution uncertainty using the BNN uncertainty [8]. Firstly, we optimize the parameters of the simple distribution instead of optimizing the original neural network’s parameters in BNN, where the posterior _p_ ( **_W_** _|_ **_X_** _,_ **_Y_** ) is fitted with a simple distribution _q_ **_θ_**<sup>_∗_(</sup><sup>**_W_**),parameterizedby</sup><sup>**_θ_**.</sup> Then by the Dropout in BNN, which can be interpreted as a variational Bayesian approximation, epistemic uncertainty can 

Similarly, the valuation function can be calculated by: 


![](assets/TMC23/TMC23.pdf-0010-23.png)


Thus, we can extend the VAP for various online ML models as long as they can calculate prediction uncertainty, such as GPR and the model under the Bayesian framework. More intuitively, rather than collecting data for significantly reducing the parameter distribution’s differential entropy, we marginally seek the data for which the model is most uncertain about the predictions. 

Authorized licensed use limited to: Shanghai Jiaotong University. Downloaded on October 18,2023 at 01:05:52 UTC from IEEE Xplore.  Restrictions apply. 

© 2023 IEEE. Personal use is permitted, but republication/redistribution requires IEEE permission.��See https://www.ieee.org/publications/rights/index.html for more information. 

This article has been accepted for publication in IEEE Transactions on Mobile Computing. This is the author's version which has not been fully edited and content may change prior to final publication. Citation information: DOI 10.1109/TMC.2023.3316145 

11 

IEEE TRANSACTION ON MOBILE COMPUTING, VOL. XXX, NO. XXX, XXX 

If there is a higher degree of uncertainty about the prediction of arriving data, we do not have enough data whose features are similar to its features, so we have less confidence in it. So when we add this data to our training data set, it will significantly reduce the model uncertainty in this data region. Thus, such data will contribute more to the model, leading to more entropy reduction of parameter distribution, and the service provider would like to post a higher price for it. In addition to online learning models, VAP can be used in some other domains to guide the data collection process. For example, in domains such as active learning [46] and Bayesian reinforcement learning [47], where the model should have the ability to identify the most valuable data for model training and add it to the training set. 

## **6 Evaluation Results** 

In this section, we evaluate our VAP through extensive experiments on real-world human behavior indicators data, which can be involved in mHealth. 

### **6.1 Evaluation Setup** 

We present the evaluation results based on two real-world human behavior data sets: 1) Human Activity Recognition (HAR) database [48], a data set built from the recordings of 30 data contributors performing daily living activities while carrying a waist-mounted smartphone with embedded inertial sensors. The obtained data set was randomly partitioned into two sets, where 70% of the volunteers were selected to generate the training data and 30% the test data. 2) Pima Indians Diabetes (PID) [49], a data set initially from the National Institute of Diabetes and Digestive and Kidney Diseases. The data set’s objective is to diagnostically predict whether a patient has diabetes based on specific diagnostic measurements included in the data set. 

### **6.2 Results of Data Valuation** 

### _6.2.1 VAP on Different Models and Tasks_ 

We evaluate the performance of VAP-Valuation. Fig. 3 shows that VAP-Valuation is a proper model value evaluation metric leading to smaller model uncertainty and higher model accuracy. First, as for RC, in Fig. 3(a) and Fig. 3(d), the general trend in total entropy reduction and prediction accuracy boost is consistent, which means the goals of data collection and model optimization are consistent under VAP. Meanwhile, in Fig. 3(b) and Fig. 3(e), by observing that the model accuracy increases slowly with the decrease of VAP-Valuation and that the turning points of them are close (for about 20 in Fig. 3(a) and 500 in Fig. 3(c), we can conclude that the VAP is able to judge the proper scale of the data collection. That is to say, after collecting such an amount of data, the valuation of the new data is relatively small, and the accuracy of the model is relatively stabilized. 

As for GPC and BNN, using the VAP-Valuation in Section 5, we value the data on the outcome space. As the PID is a smaller data set, we adopt the GPC model to it. Meanwhile, HAR is a more extensive data set, which is more suitable for training with the BNN model. In Fig. 3(c) and Fig. 3(f), we can get a similar result with the RC model. By adding a new data sample, the model uncertainty is smaller, leading each data’s contribution to the model more negligible, and the model accuracy increases. Also, the turning points of them are close, for about 20 in Fig. 3(c) and 1000 in Fig. 3(f). Moreover, from all the results in these 

three models, we can notice that the contribution of each data point shows the characteristic of diminishing marginal, which is consistent with the properties we described in Section 3.2. Valuation on the outcome space (Fig. 3(c) and Fig. 3(f)) appears to fluctuate more than the valuation on the parameter space because there is only one parameter space, and its dimension is higher and the previous decline is more. While the predictive distribution for each data is a different distribution. We can also notice some prominent high points in VAP-Valuation. Such data points may be the data points of new distributions in the system that have not been acquired before. In practice, in addition to data points that may be of higher epistemic uncertainty and thus show high value to the model, it can also be some incorrect data due to the problems arising from equipment acquisition. Furthermore, the service provider can identify and distinguish between the two types of data based on specific tasks. For example, the service provider can distinguish whether data is from a hypertensive patient (150/100 mmHg) or is derived from an abnormal collection (500/100 mmHg). 

### _6.2.2 Performance of Different Data Valuation Metrics_ 

We compare our method with other static data valuation metrics for machine learning, including TMC-Shapley [20], G- Shapley [20] and Random (one possible online metric) in Fig. 4. Compared with other methods, VAP-Valuation is more suitable for online learning for the following reasons. First, as Fig. 4(a) shows, the VAP-Valuation shows many excellent characteristics for data pricing and collection. It has a significant downward trend as the gradual increase of data over time considers the arrival order, which can incentive an earlier data submission. Besides, we can see that VAP-Valuation is always strictly positive, which provides convenience for data pricing. 

Moreover, Shapley value and its variants are common practices in data valuation for the ML field, so here we emphasize why VAP outperforms Shapley in online learning tasks. Compared to the Shapley value, VAP-Valuation can perform online calculations without corresponding labels and testing data according to the inferrability of VAP-Valuation we mentioned in 3.2. Simultaneously, the computational complexity will increase significantly with the larger scale of the data set in static Shapely value. Although there are some approximate calculation methods such as TMC-Shapley [20], it still requires a lot of test data and high computational cost, which is impossible and inappropriate to achieve in a real-world mHealth system. G-Shapley, an approximation of TMC-Shapley, can be adapted to online learning. The marginal contribution in G-Shapley is the change of the model’s performance. However, as shown in Fig. 4(a), we can find the G- Shapley does not achieve a good approximation of TMC-Shapley, because the calculation result can be affected by various factors, the size of the test set, learning rate, haphazard, etc. Finally, We can see that VAP-Valuation consistently outperforms the other two mechanisms as illustrated in Fig. 4(b), as it shows a better decrease over time than others as removing high-valuation data points. Thus, VAP-Valuation is more suitable for online learning tasks. 

### **6.3 Results of Data Pricing** 

First, we compare the performance of different data pricing mechanisms under a regular situation: VAP-Pricing, Random, Half Fix, Half Valuation, LinUCB [41] and UCB1 [40]. In Random 

Authorized licensed use limited to: Shanghai Jiaotong University. Downloaded on October 18,2023 at 01:05:52 UTC from IEEE Xplore.  Restrictions apply. © 2023 IEEE. Personal use is permitted, but republication/redistribution requires IEEE permission.��See https://www.ieee.org/publications/rights/index.html for more information. 

This article has been accepted for publication in IEEE Transactions on Mobile Computing. This is the author's version which has not been fully edited and content may change prior to final publication. Citation information: DOI 10.1109/TMC.2023.3316145 

IEEE TRANSACTION ON MOBILE COMPUTING, VOL. XXX, NO. XXX, XXX 

12 


![](assets/TMC23/TMC23.pdf-0012-03.png)


<!-- Start of picture text -->
0.80 0.20 0.80 0.7 0.80<br>4 0.6<br>0.75 0.15 0.75 0.5 0.75<br>3<br>2 0.70 0.10 VAP-ValuationAccuracy 0.70 0.40.3 VAPAccuracy-Valuation 0.70<br>1 VAP-Valuation 0.05 0.2 0.65<br>0.65 0.65<br>Accuracy 0.1 0.60<br>0 0.00<br>0 100 200 300 400 500 600 0 100 200 300 400 500 600 0 100 200 300 400 500 600<br>Data Sample Data Sample Data Sample<br>(a) RC on PID (b) RC on PID (c) GPC on PID<br>1.0 1.0 0.150<br>500 2.0 0.9<br>0.125<br>400 0.8 1.5 0.8 0.100 0.8<br>300 0.6 1.0 VAP-Valuation Accuracy 0.6 0.075 VAPAccuracy-Valuation 0.70.6<br>200 0.050<br>0.4 0.5 0.4 0.5<br>100 VAP-Valuation 0.025<br>0.4<br>0 Accuracy 0.2 0.0 0.2 0.000 0.3<br>0 2000 4000 6000 0 2000 4000 6000 0 2000 4000 6000<br>Data Sample Data Sample Data Sample<br>(d) RC on HAR (e) RC on HAR (f) BNN on HAR<br>Accuracy Accuracy Accuracy<br>Data Valuation Data Valuation<br>Total Entropy Reduction<br>Accuracy Accuracy Accuracy<br>Data Valuation Data Valuation<br>Total Entropy Reduction<br><!-- End of picture text -->

Fig. 3. VAP-Valuation on different models (Ridge classification (RC), Gaussian process classification (GPC)) and Tasks (HAR and PID Database). 


![](assets/TMC23/TMC23.pdf-0012-05.png)


<!-- Start of picture text -->
0.08 0.10 100<br>VAP-Pricing VAP-Pricing<br>TMC-shapley 90 G-Shapley<br>0.06 G-shapley 0.05 Random<br>80<br>0.04 0.00<br>70<br>0.02 −0.05<br>60<br>0.00 −0.10 50<br>0 20 40 60 80 100 0 20 40 60 80<br>Data Sample Fraction of Data Sample Removed (%)<br>(a) (b)<br>Shapley<br>Entropy Reduction<br>Prediction Accuracy (%)<br><!-- End of picture text -->

Fig. 4. Performance of different data valuation metrics. **(a)** Comparison of the valuation of the first 100 PID data; **(b)** The effect of removing high-valuation data points under different data valuation metrics. 

pricing, the posted price _p_ is uniformly distributed within [0 _,_ 1]. In Half Fix pricing, we set _p_ = 0 _._ 5. And in Half Valuation pricing, we set _p_ = min(0 _._ 5 _· G_ **_X_** ( **_x_** ) _,_ 1). In all experiments, we set _α_ = 1 _._ 2, _ϵ_ = 0, _K_ = 10, _T_ = 500, and the reserve value is an approximately normal distribution within [0 _,_ 1], where the mean is 0 _._ 5, and the variance is 0 _._ 01 unless otherwise noted. In Fig. 5, we can see that VAP-Pricing is always better than any other policies under different settings of reserve values of data contributors. Moreover, when the reserve value distribution is closer to the constant distribution, VAP-Pricing can get a higher profit. As for other mechanisms, we can see that Random is always the worst. The performance of Half Fix will be worse than contextual methods because it cannot capture the valuation information of the data samples. It can be considered as the optimal case of the traditional UCB1 method (also without considering the context), and Fig. 5 turns out that it is true. In addition, from the last figure in Fig. 5, it can be shown that Half Fix has a very high profit in the early stage. This is because when the reserve value is a constant _f_ ( _v_ ) = 0 _._ 5, the posted price _p_ = 0 _._ 5 in each time slot will definitely be accepted by data contributors. The profit growth of Half Fix will be slow or even negative in the later period, also because the lack of data valuation results in the purchase of low-value data 

at high prices. In contrast, Half Valuation can always buy the data sample with a higher valuation by posting a high price, so it can always maintain a better growth trend. However, without the estimation of the reserve value will overbid, causing its total benefit to be damaged. Besides, the naive LinUCB method does not take into account the monotonicity of pricing and also leads to unsatisfactory profits. 

Besides, we evaluate the performance of different _ϵ_ . In Fig. 6, we can see that a bigger _ϵ_ leads to a smaller budget and total entropy reduction while maintaining a high profit. Supposing that the service provider chooses a higher _ϵ_ , correspondingly, he tends to use the limited budget to collect a smaller data set, this limited data set can effectively reduce the uncertainty of model predictions. On the contrary, if the service provider chooses a smaller _ϵ_ , he wants to use more budget to collect more data. This adequate data set can further significantly reduce the uncertainty. 

Comparing the price of different pricing policies in Fig. 7, we can see that the VAP-Pricing method can maintain the downward trend of valuation compared to Half Valuation, which is also fairer than other Random or Half Fix. Compared with other advanced bandit methods, _i.e._ , UCB1 and LinUCB, VAP-Pricing can better estimate the reserve value distribution of contributors, leading to faster convergence and a more reasonable price. It can monitor changes in data valuation and adjust the posted price promptly to maximize the profit. 

In order to explain the effect of VAP-Pricing more intuitively, we also designed a set of experiments in a special case, that is when the reserve value _v_ = 0. Fig. 8 shows that VAP-Pricing can converge quickly to the lowest price to extract more profit. 

As for the performance of different data pricing mechanisms under a fixed limited budget, we compare the performances of VAP-Pricing, Random, Half Fix, Half Valuation, LinUCB, UCB1, and VAP-PricingwK in Fig. 9. VAP-PricingwK shows demonstrates exceptional budget control capability, consistently halting close to the predetermined timeframe ( _T_ = 500), contrasting with other methods that cease earlier due to budget exhaustion. Concurrently, the total profit of VAP-PricngwK is maximal and 

Authorized licensed use limited to: Shanghai Jiaotong University. Downloaded on October 18,2023 at 01:05:52 UTC from IEEE Xplore.  Restrictions apply. © 2023 IEEE. Personal use is permitted, but republication/redistribution requires IEEE permission.��See https://www.ieee.org/publications/rights/index.html for more information. 

This article has been accepted for publication in IEEE Transactions on Mobile Computing. This is the author's version which has not been fully edited and content may change prior to final publication. Citation information: DOI 10.1109/TMC.2023.3316145 

IEEE TRANSACTION ON MOBILE COMPUTING, VOL. XXX, NO. XXX, XXX 

13 


![](assets/TMC23/TMC23.pdf-0013-03.png)


<!-- Start of picture text -->
160 VAP-Pricing 175 VAP-Pricing 200 VAP-Pricing<br>140 Random 150 Random 175 Random<br>Half Fix Half Fix Half Fix<br>120 Half Valuation 125 Half Valuation 150 Half Valuation<br>LinUCB LinUCB LinUCB<br>100 UCB1 100 UCB1 125 UCB1<br>80 100<br>75<br>60 75<br>50<br>40 50<br>20 25 25<br>0 0 0<br>0 100 200 300 400 500 0 100 200 300 400 500 0 100 200 300 400 500<br>Data Sample Data Sample Data Sample<br>Total Profit Total Profit Total Profit<br><!-- End of picture text -->

Fig. 5. Performance of different data pricing mechanisms under different reserve values’ distribution, from left to right: _f_ 1( _v_ ): An approximately normal distribution within [0 _,_ 1], where the mean is 0 _._ 5, and variance is 0 _._ 1; _f_ 2( _v_ ): An approximately normal distribution within [0 _,_ 1], where the mean is 0 _._ 5, and variance is 0 _._ 01; A constant distribution as _f_ 3( _v_ ) = 0 _._ 5. 


![](assets/TMC23/TMC23.pdf-0013-05.png)


<!-- Start of picture text -->
1.0<br>150 ϵ=0 ϵ=0.1 300 ϵϵ=0.1=0 0.5<br>ϵ=0.5 ϵ=0.5 0 100 200 300 400 500<br>200<br>100 Data Sample<br>1.0<br>50 100 0.5<br>0 0 0 100 200 300 400 500<br>0 200 400 0 200 400 Data Sample<br>Data Sample Data Sample<br>0.5<br>150 ϵϵ=0.1=0 300 0.0 0 100 200 300 400 500<br>ϵ=0.5 Data Sample<br>100 200 1.0<br>0.5<br>50 100 ϵ=0<br>ϵ=0.1 0 100 200 300 400 500<br>ϵ=0.5 Data Sample<br>0 0 1.0<br>0 200 400 0 200 400<br>Data Sample Data Sample 0.5<br>0 100 200 300 400 500<br>150 ϵ=0 ϵ=0.1 300 Data Sample<br>ϵ=0.5<br>100<br>200<br>Fig. 7. Price Comparison of Different Pricing Mechanisms (From top to bottom<br>50 100 ϵ=0 are VAP-Pricing, Half Valuation, Random, LinUCB, and UCB1).<br>ϵ=0.1<br>ϵ=0.5<br>0 0<br>0 200 400 0 200 400<br>Data Sample Data Sample thus obtaining larger profits.<br>Price<br>Budget<br>Price<br>Total Entropy Reduction<br>Price<br>Budget Price<br>Total Entropy Reduction<br>Price<br>Budget<br>Total Entropy Reduction<br><!-- End of picture text -->

Fig. 7. Price Comparison of Different Pricing Mechanisms (From top to bottom are VAP-Pricing, Half Valuation, Random, LinUCB, and UCB1). 

thus obtaining larger profits. 

Fig. 6. Performance of Different _ϵ_ ( _ϵ_ = 0, 0.1, 0.5) and different reserve values’ distribution (From top to bottom are _f_ 1( _v_ ), _f_ 2( _v_ ), and _f_ 3( _v_ )) on budget and entropy reduction. 

the UCB1 and random methods are the worst. In addition, it can be noticed that VAP-PricingwK does not grow as fast as some of the other algorithms in the early stages due to the need to control the budget and not to adopt a particularly aggressive exploration strategy, but since it retains a larger budget, it will have the opportunity to collect valuable data for higher profits in the later stages. It is also worth noting that although VAPPricing consumes the budget more rapidly, the performance is acceptable. This is ascribed to the incorporation of contextual information, which enhances learning speed. However, under a fixed budget, it is challenging to identify an appropriate budget control factor _ϵ_ for VAP-Pricing in advance, resulting in a loss of final profit. Conversely, VAP-PricingwK’s control under a fixed budget is automatic. Finally, we also find that when the variance of the reserve value _v_ is smaller, the magnitude of the change is smaller, making it easier for VAP-PricingwK to estimate _Fv_ ( _pi_ ), 

## **7 Related Work** 

### **7.1 Mobile Health** 

The researchers develop multiple models by combining principled medical approaches with ML techniques in mHealth in a variety of domains, including diabetes [50], [51], [52], activity recognition [53], [54], depression treatment [55], [56], and blood pressure monitoring [31], [57]. Recently, researchers are making recent progress in COVID-19 [7], [58], [59], [60]. The design of the mobile device not only proposes a viable mHealth solution and drives the further development of mHealth, but also generates a large amount of mHealth data in the process. Based on such massive data, various machine learning models have been developed, especially some online learning models and incremental learning models are proposed [14], [15], [16], [17], in which the mHealth models would continuously update over time as more information is collected and made available. There are also many researchers who focus on the integration of Bayesian methods into mobile health [61], [62], [63]. However, these works are currently considering designs of hardware devices and ML models’ improvements. Few of them consider the data 

Authorized licensed use limited to: Shanghai Jiaotong University. Downloaded on October 18,2023 at 01:05:52 UTC from IEEE Xplore.  Restrictions apply. © 2023 IEEE. Personal use is permitted, but republication/redistribution requires IEEE permission.��See https://www.ieee.org/publications/rights/index.html for more information. 

This article has been accepted for publication in IEEE Transactions on Mobile Computing. This is the author's version which has not been fully edited and content may change prior to final publication. Citation information: DOI 10.1109/TMC.2023.3316145 

IEEE TRANSACTION ON MOBILE COMPUTING, VOL. XXX, NO. XXX, XXX 

14 


![](assets/TMC23/TMC23.pdf-0014-03.png)


<!-- Start of picture text -->
350 VAP-Pricing<br>Random<br>300 Half Fix<br>Half Valuation<br>250 LinUCB<br>UCB1<br>200<br>150<br>100<br>50<br>0<br>0 100 200 300 400 500<br>Data Sample<br>1.0<br>0.5<br>0 100 200 300 400 500<br>Data Sample<br>1.0<br>0.5<br>0 100 200 300 400 500<br>Data Sample<br>1.0<br>0.5<br>0 100 200 300 400 500<br>Data Sample<br>Total Profit<br>Price<br>Price<br>Price<br><!-- End of picture text -->

Aleatoric uncertainty cannot be reduced even if more data were to be collected. While epistemic uncertainty comes from the model’s ignorance of the data when the collected data is not enough. This uncertainty can be explained away given enough data and is often referred to as model uncertainty. These two uncertainties were first studied and classified by Kiureghian and Ditlevsen [68]. And these two types of uncertainty have further been more specifically studied in bayesian deep learning for computer vision by Kendall and Gal [69]. Before that, Gal and Ghahramani proved that deep neural networks could be cast as performing approximate variational inference in a Bayesian setting [70] and extend it to arbitrary deep learning models [71]. Based on that, they model uncertainty with dropout NNs [72]. In previous work, uncertainty is the predictive distribution variance in the prediction task for the current test data to judge the credibility of a prediction. However, in VAP-Valuation, we calculate the posterior distribution entropy reduction of parameter or the predictive distribution variance of new data to measure each data’s contribution. 

### **7.4 Multi-armed Bandits** 

Fig. 8. Performance and Price when reserve value _f_ 4( _v_ )=0. 

acquisition mechanism, neither data valuation, and data pricing mechanism. Barriers still exist in the journey of mHealth data from generation to use. 

### **7.2 Data Valuation and Pricing for ML Tasks** 

Lately, Shapley value has been widely used in the data valuation and pricing problem for ML tasks. Agarwal _et al._ [18] design a market mechanism to price training data and match buyers to sellers based on Shapley value. Jia _et al._ introduce several additional approximation methods for efficient computation of Shapley values for training data [19]; subsequently, they provided an algorithm for the exact computation of Shapley values for the specific case of nearest-neighbour classifiers [22]. Meanwhile, Ghorbani _et al._ developed a truncated Monte Carlo sampling scheme (TMC-Shapley), demonstrating empirical effectiveness across various ML tasks [20]; subsequently, they proposed distributional Shapley, where the value of a point is defined in the context of an underlying data distribution [21]. However, these data valuation methods are not suitable for online ML tasks. Despite not being used for data valuation, ranking the importance of training data points has been used for understanding model behaviors, detecting data set errors, etc. Existing methods include using the influence function [64] for smooth parametric models, and a variant [65] for non-parametric ones. Ogawa _et al._ [66] proposed rules to identify and remove the least influential data to reduce the computation cost when training support vector machines (SVM). Kendall _et al._ measured the uncertainties in Bayesian deep learning for computer vision [67]. These approaches could potentially be used for valuing data. 

### **7.3 Uncertainty in Machine Learning** 

The VAP-Valuation metric is closely related to the concept of epistemic uncertainty in machine Learning. In Bayesian modeling, there are two main types of uncertainty one can model. Aleatoric uncertainty comes from the noise when data is generated or collected, for example, sensor noise or motion noise. 

The multi-armed bandit (MAB) problem is a sequential decisionmaking model and widely studied by many works with different models and solutions, such as upper confidence bound [40], _ϵ_ - greedy [73], and Thompson sampling [74], [75]. In the traditional setting of MAB, an arm can be represented by a scalar to infer the reward that is drawn from its distribution which is unknown to the player, while in the contextual bandit [41], [43], a context vector represents each arm, and _O_<sup>˜</sup> ( _√T_ ) regret bounds can be achieved based on UCB. Moreover, as classical modeling, the linear reward model has been widely studied in contextual bandits [76], [77]. Considering knapsack constraints on various resources in the bandit framework, the bandit with knapsack (BwK) is first studied by Badanidiyuru _et al._ [78], who presented two algorithms and proved that the regret achieved by both algorithms is optimal up to polylogarithmic factors. Later, based on the optimal regret, Agrawal and Devanur further proposed alternative optimal algorithms under concave rewards convex knapsacks [45], and a linear contextual setting [44]. Many real-world problems can be modeled as various versions of bandit problems [79], [80], [81], because MAB represents an online learning paradigm that naturally captures the intrinsic exploration-exploitation tradeoff in sequential decision-making process. 

## **8 Conclusion** 

In this work, we have introduced VAP, an innovative online data valuation and pricing mechanism designed specifically for ML tasks in the context of mobile health (mHealth). We value the data by measuring its contribution to the ML model under the Bayesian perspective, using the entropy of the distributions over model parameters. To address the profit maximization problem, we have developed an online posted price data pricing mechanism within a contextual multi-armed bandit framework, leveraging the data valuation metric provided by VAP. And further, for the limited budget situation, we have proposed VAP-PricingwK under a multi-armed bandit with a knapsack framework. Moreover, we have extended VAP from Bayesian linear regression to more complex ML models by computing the entropy from the parameter space to the prediction space. 

Authorized licensed use limited to: Shanghai Jiaotong University. Downloaded on October 18,2023 at 01:05:52 UTC from IEEE Xplore.  Restrictions apply. © 2023 IEEE. Personal use is permitted, but republication/redistribution requires IEEE permission.��See https://www.ieee.org/publications/rights/index.html for more information. 

This article has been accepted for publication in IEEE Transactions on Mobile Computing. This is the author's version which has not been fully edited and content may change prior to final publication. Citation information: DOI 10.1109/TMC.2023.3316145 

IEEE TRANSACTION ON MOBILE COMPUTING, VOL. XXX, NO. XXX, XXX 

15 


![](assets/TMC23/TMC23.pdf-0015-03.png)


<!-- Start of picture text -->
140 140 175<br>120 120 150<br>100 100 125<br>80 80 100<br>60 VAP-PricinRandom g 60 VAP-Pricing Random 75 VAP-PricingRandom<br>Half Fix Half Fix Half Fix<br>40 Half Valuation 40 Half Valuation 50 Half Valuation<br>20 LinUCB 20 LinUCB 25 LinUCB<br>UCB1 UCB1 UCB1<br>0 VAP-PricingwK 0 VAP-PricingwK 0 VAP-PricingwK<br>0 100 200 300 400 500 0 100 200 300 400 500 0 100 200 300 400 500<br>Data Sample Data Sample Data Sample<br>Total Profit Total Profit Total Profit<br><!-- End of picture text -->

Fig. 9. Performance of different data pricing mechanisms under a fixed limited budget _B_ = 100. Reserve values’ distributions from left to right are _f_ 1( _v_ ), _f_ 2( _v_ ), and _f_ 3( _v_ ). 

Through comprehensive evaluation, we have demonstrated that VAP outperforms existing online data valuation and pricing mechanisms. The results highlight the effectiveness and superiority of our approach in the mHealth domain. 

- [19] R. Jia, D. Dao, B. Wang, F. A. Hubis, N. Hynes, N. M. G¨urel, B. Li, C. Zhang, D. Song, and C. J. Spanos, “Towards efficient data valuation based on the shapley value,” in _AISTATS_ , 2019, pp. 1167–1176. 

- [20] A. Ghorbani and J. Y. Zou, “Data shapley: Equitable valuation of data for machine learning,” in _ICML_ , 2019, pp. 2242–2251. 

- [21] A. Ghorbani, M. P. Kim, and J. Zou, “A distributional framework for data valuation,” in _ICML_ , 2020, pp. 3535–3544. 

## **References** 

- [1] S. Kumar, W. Nilsen, M. Pavel, and M. B. Srivastava, “Mobile health: Revolutionizing healthcare through transdisciplinary research,” _Computer_ , vol. 46, no. 1, pp. 28–35, 2013. 

- [2] “Apple health,” https://www.apple.com/ios/health/. 

- [3] “Google fit,” https://www.google.com/fit/. 

- [4] “Microsoft health,” https://www.microsoft.com/en-us/industry/health/ microsoft-cloud-for-healthcare. 

- [5] R. S. Istepanian and T. Al-Anzi, “m-health 2.0: new perspectives on mobile health, machine learning and big data analytics,” _Methods_ , vol. 151, pp. 34–40, 2018. 

- [6] Q. Wu, X. Chen, Z. Zhou, and J. Zhang, “Fedhome: Cloud-edge based personalized federated learning for in-home health monitoring,” _IEEE Transactions on Mobile Computing_ , vol. 21, no. 8, pp. 2818–2832, 2020. 

- [7] C. Brown, J. Chauhan, A. Grammenos, J. Han, A. Hasthanasombat, D. Spathis, T. Xia, P. Cicuta, and C. Mascolo, “Exploring automatic diagnosis of COVID-19 from crowdsourced respiratory sound data,” in _KDD_ , 2020, pp. 3474–3484. 

- [8] Y. Gal, “Uncertainty in deep learning,” _University of Cambridge_ , vol. 1, no. 3, 2016. 

- [9] G. Litjens, T. Kooi, B. E. Bejnordi, A. A. A. Setio, F. Ciompi, M. Ghafoorian, J. A. van der Laak, B. van Ginneken, and C. I. S´anchez, “A survey on deep learning in medical image analysis,” _Med Image Anal_ , vol. 42, pp. 60 – 88, 2017. 

- [10] D. C. Mohr, M. Zhang, and S. M. Schueller, “Personal sensing: understanding mental health using ubiquitous sensors and machine learning,” _Annu. Rev. Clin. Psychol._ , vol. 13, pp. 23–47, 2017. 

- [11] G. Xing, “Tackling the challenges of machine learning for mobile health systems,” in _HealthDL_ , 2020. 

- [12] S. Arora, J. Yttri, and W. Nilsen, “Privacy and security in mobile health (mhealth) research,” _Alcohol research: current reviews_ , vol. 36, no. 1, p. 143, 2014. 

- [13] S. Kumar, W. J. Nilsen, A. Abernethy, A. Atienza, K. Patrick, M. Pavel, W. T. Riley, A. Shar, B. Spring, D. Spruijt-Metz _et al._ , “Mobile health technology evaluation: the mhealth evidence workshop,” _Am J Prev Med_ , vol. 45, no. 2, pp. 228–236, 2013. 

- [14] C. Hu, Y. Chen, L. Hu, and X. Peng, “A novel random forests based class incremental learning method for activity recognition,” _Pattern Recognit._ , vol. 78, pp. 277–290, 2018. 

- [15] D. A. Jenkins, M. Sperrin, G. P. Martin, and N. Peek, “Dynamic models to predict health outcomes: current status and methodological challenges,” _Diagn Progn Res_ , vol. 2, no. 1, p. 23, 2018. 

- [16] K. Y. Ngiam and W. Khor, “Big data and machine learning algorithms for health-care delivery,” _Lancet Oncol._ , vol. 20, no. 5, pp. e262–e273, 2019. 

- [17] S. Srinivasan, K. R. Srivatsa, I. V. R. Kumar, R. Bhargavi, and V. Vaidehi, “A regression based adaptive incremental algorithm for health abnormality prediction,” in _ICRTIT_ , 2013, pp. 690–695. 

- [18] A. Agarwal, M. Dahleh, and T. Sarkar, “A marketplace for data: An algorithmic solution,” in _EC_ , 2019, pp. 701–726. 

- [22] R. Jia, D. Dao, B. Wang, F. A. Hubis, N. M. G¨urel, B. Li, C. Zhang, C. J. Spanos, and D. Song, “Efficient task-specific data valuation for nearest neighbor algorithms,” _Proc. VLDB Endow._ , vol. 12, no. 11, pp. 1610–1623, 2019. 

- [23] P. Dubey, “On the uniqueness of the shapley value,” _Int. J. Game Theory_ , vol. 4, no. 3, pp. 131–139, 1975. 

- [24] A. V. Goldberg, J. D. Hartline, and A. Wright, “Competitive auctions and digital goods,” in _SODA_ , 2001, pp. 735–744. 

- [25] S. Alaei, A. Malekian, and A. Srinivasan, “On random sampling auctions for digital goods,” in _EC_ , 2009, pp. 187–196. 

- [26] R. Kleinberg and T. Leighton, “The value of knowing a demand curve: bounds on regret for online posted-price auctions,” in _FOCS_ , 2003, pp. 594–605. 

- [27] A. Xu, Z. Zheng, F. Wu, and G. Chen, “Online data valuation and pricing for machine learning tasks in mobile health,” in _INFOCOM_ , 2022, pp. 850–859. 

- [28] R. Kleinberg and T. Leighton, “The value of knowing a demand curve: Bounds on regret for online posted-price auctions,” in _FOCS_ , 2003, pp. 594–605. 

- [29] J. D. Hartline and B. Lucier, “Bayesian algorithmic mechanism design,” in _STOC_ , 2010, pp. 301–310. 

- [30] S. A. Baldwin and M. J. Larson, “An introduction to using bayesian linear regression with clinical data,” _Behaviour research and therapy_ , vol. 98, pp. 58–75, 2017. 

- [31] M. Kachuee, M. M. Kiani, H. Mohammadzade, and M. Shabany, “Cuffless blood pressure estimation algorithms for continuous health-care monitoring,” _IEEE. Trans. Biomed. Eng._ , vol. 64, no. 4, pp. 859–869, 2017. 

- [32] W. Wang, S. Mirjafari, G. Harari, D. Ben-Zeev, R. Brian, T. Choudhury, M. Hauser, J. Kane, K. Masaba, S. Nepal _et al._ , “Social sensing: Assessing social functioning of patients living with schizophrenia using mobile phone sensing,” in _CHI_ , 2020, pp. 1–15. 

- [33] J. Q. Candela and C. E. Rasmussen, “A unifying view of sparse approximate gaussian process regression,” _J. Mach. Learn. Res._ , vol. 6, pp. 1939–1959, 2005. 

- [34] I. Kononenko, “Bayesian neural networks,” _Biological Cybernetics_ , vol. 61, no. 5, pp. 361–370, 1989. 

- [35] G. C. McDonald, “Ridge regression,” _Wiley Interdiscip. Rev. Comput. Stat._ , vol. 1, no. 1, pp. 93–100, 2009. 

- [36] T. M. Cover and J. A. Thomas, _Elements of Information Theory_ . Wiley, 2001. 

- [37] S. Fujishige, _Submodular functions and optimization_ . Elsevier, 2005. [38] S. Bubeck and N. Cesa-Bianchi, “Regret analysis of stochastic and nonstochastic multi-armed bandit problems,” _Found. Trends Mach. Learn._ , vol. 5, no. 1, pp. 1–122, 2012. 

- [39] L. Xu, C. Jiang, Y. Qian, Y. Zhao, J. Li, and Y. Ren, “Dynamic privacy pricing: A multi-armed bandit approach with time-variant rewards,” _IEEE Trans. Inf. Forensics Secur._ , pp. 271–285, 2017. 

- [40] P. Auer, N. Cesa-Bianchi, and P. Fischer, “Finite-time analysis of the multiarmed bandit problem,” _Mach. Learn._ , vol. 47, no. 2-3, pp. 235–256, 2002. 

Authorized licensed use limited to: Shanghai Jiaotong University. Downloaded on October 18,2023 at 01:05:52 UTC from IEEE Xplore.  Restrictions apply. © 2023 IEEE. Personal use is permitted, but republication/redistribution requires IEEE permission.��See https://www.ieee.org/publications/rights/index.html for more information. 

This article has been accepted for publication in IEEE Transactions on Mobile Computing. This is the author's version which has not been fully edited and content may change prior to final publication. Citation information: DOI 10.1109/TMC.2023.3316145 

16 

IEEE TRANSACTION ON MOBILE COMPUTING, VOL. XXX, NO. XXX, XXX 

- [41] L. Li, W. Chu, J. Langford, and R. E. Schapire, “A contextual-bandit approach to personalized news article recommendation,” in _WWW_ , 2010, pp. 661–670. 

- [42] T. M. Rassias and T. M. Rassias, _Functional equations, inequalities, and applications_ . Springer, 2003. 

- [43] Y. Abbasi-Yadkori, D. P´al, and C. Szepesv´ari, “Improved algorithms for linear stochastic bandits,” in _NeurIPS_ , 2011. 

- [44] S. Agrawal and N. Devanur, “Linear contextual bandits with knapsacks,” in _NeurIPS_ , 2016. 

- [45] S. Agrawal and N. R. Devanur, “Bandits with concave rewards and convex knapsacks,” in _EC_ , 2014, pp. 989–1006. 

- [46] D. Golovin, A. Krause, and D. Ray, “Near-optimal bayesian active learning with noisy observations,” in _NeurIPS_ , 2010, pp. 766–774. 

- [47] G. Chalkiadakis and C. Boutilier, “Bayesian reinforcement learning for coalition formation under uncertainty,” in _AAMAS_ , 2004, pp. 1090–1097. 

- [48] D. Anguita, A. Ghio, L. Oneto, X. Parra, and J. L. Reyes-Ortiz, “A public domain dataset for human activity recognition using smartphones.” in _Esann_ , vol. 3, 2013, p. 3. 

- [49] J. W. Smith, J. Everhart, W. Dickson, W. Knowler, and R. Johannes, “Using the adap learning algorithm to forecast the onset of diabetes mellitus,” in _Proc Annu Symp Comput Appl Med Care_ , 1988, p. 261. 

- [50] D. Preuveneers and Y. Berbers, “Mobile phones assisting with health self-care: a diabetes case study,” in _HCI_ , G. H. ter Hofte, I. Mulder, and B. E. R. de Ruyter, Eds., 2008. 

- [51] S. Kitsiou, G. Par´e, M. Jaana, and B. Gerber, “Effectiveness of mhealth interventions for patients with diabetes: an overview of systematic reviews,” _PloS one_ , p. e0173160, 2017. 

- [52] M. J. Reading, E. M. Heitkemper, M. Lor, and L. Mamykina, “Exploring mhealth intervention designs to engage low-income, minority adults with type 2 diabetes in self-monitoring,” in _AMIA_ , 2018. 

- [53] U. Fareed, “Smartphone sensor fusion based activity recognition system for elderly healthcare,” in _MobileHealth@MobiHoc_ , 2015, pp. 29–34. 

   - [69] A. Kendall and Y. Gal, “What uncertainties do we need in bayesian deep learning for computer vision?” in _NeurIPS_ , 2017, pp. 5574–5584. 

   - [70] Y. Gal and Z. Ghahramani, “Dropout as a bayesian approximation: Insights and applications,” in _Deep Learning Workshop, ICML_ , 2015. 

   - [71] ——, “On modern deep learning and variational inference,” in _Advances in Approximate Bayesian Inference workshop, NeurIPS_ , 2015. 

   - [72] ——, “Dropout as a bayesian approximation: Representing model uncertainty in deep learning,” in _ICML_ , 2016, pp. 1050–1059. 

   - [73] J. Langford and T. Zhang, “The epoch-greedy algorithm for multi-armed bandits with side information,” _NeurIPS_ , 2007. 

   - [74] S. Agrawal and N. Goyal, “Thompson sampling for contextual bandits with linear payoffs,” in _ICML_ , 2013, pp. 127–135. 

   - [75] W. R. Thompson, “On the likelihood that one unknown probability exceeds another in view of the evidence of two samples,” _Biometrika_ , vol. 25, no. 3-4, pp. 285–294, 1933. 

   - [76] W. Chu, L. Li, L. Reyzin, and R. E. Schapire, “Contextual bandits with linear payoff functions,” in _AISTATS_ , 2011, pp. 208–214. 

   - [77] S. Agrawal and N. Goyal, “Thompson sampling for contextual bandits with linear payoffs,” in _ICML_ , 2013, pp. 127–135. 

   - [78] A. Badanidiyuru, R. Kleinberg, and A. Slivkins, “Bandits with knapsacks,” in _FOCS_ , 2013, pp. 207–216. 

   - [79] H. Wang, Y. Yang, E. Wang, W. Liu, Y. Xu, and J. Wu, “Truthful user recruitment for cooperative crowdsensing task: A combinatorial multiarmed bandit approach,” _IEEE Transactions on Mobile Computing_ , vol. 22, no. 7, pp. 4314–4331, 2023. 

   - [80] C. Zeng, Q. Wang, S. Mokhtari, and T. Li, “Online context-aware recommendation with time varying multi-armed bandit,” in _KDD_ , 2016, pp. 2025–2034. 

   - [81] F. Vannella, A. Prouti`ere, Y. Jedra, and J. Jeong, “Learning optimal antenna tilt control policies: A contextual linear bandit approach,” in _INFOCOM_ , 2022, pp. 740–749. 

- [54] S. Laskaridis, D. Spathis, and M. Almeida, “Federated mobile sensing for activity recognition,” in _MobiCom_ , 2021, pp. 858–859. 

- [55] R. Wang, W. Wang, A. DaSilva, J. F. Huckins, W. M. Kelley, T. F. Heatherton, and A. T. Campbell, “Tracking depression dynamics in college students using mobile phone and wearable sensing,” _Proc. ACM Interact. Mob. Wearable Ubiquitous Technol._ , vol. 2, no. 1, pp. 43:1–43:26, 2018. 

- [56] A. C. Myers, L. Chesebrough, R. Hu, M. R. Turchioe, J. Pathak, and R. M. Creber, “Evaluating commercially available mobile apps for depression self-management,” in _AMIA_ , 2020. 

- [57] N. Bui, N. Pham, J. J. Barnitz, Z. Zou, P. Nguyen, H. Truong, T. Kim, N. Farrow, A. Nguyen, J. Xiao, R. R. Deterding, T. N. Dinh, and T. Vu, “ebp: A wearable system for frequent and comfortable blood pressure monitoring from user’s ear,” in _MobiCom_ , 2019, pp. 1–17. 

- [58] A. Asadzadeh and L. R. Kalankesh, “A scope of mobile health solutions in covid-19 pandemics,” _Informatics in medicine unlocked_ , p. 100558, 2021. 


![](assets/TMC23/TMC23.pdf-0016-32.png)


**Anran Xu** is a Ph.D candidate in the Department of Computer Science and Engineering at Shanghai Jiao Tong University, P. R. China. She received her B.S. degree in Software Engineering from Shandong University, P.R.China, in 2019. Her research interests include algorithmic game theory, mobile computing, and computational advertising. For more information, please visit https://anran-xu.github.io/ 

- [59] A. Raposo, L. Marques, R. Correia, F. Melo, J. Valente, T. Pereira, L. B. Ros´ario, F. Froes, J. Sanches, and H. P. d. Silva, “e-covig: a novel mhealth system for remote monitoring of symptoms in covid-19,” _Sensors_ , p. 3397, 2021. 

- [60] C. P. Adans-Dester, S. Bamberg, F. P. Bertacchi, B. Caulfield, K. Chappie, D. Demarchi, M. K. Erb, J. Estrada, E. E. Fabara, M. Freni _et al._ , “Can mhealth technology help mitigate the effects of the covid-19 pandemic?” _IEEE Open J. Eng. Med. Biol._ , pp. 243–248, 2020. 

- [61] A. N. Repaka, S. D. Ravikanti, and R. G. Franklin, “Design and implementing heart disease prediction using naives bayesian,” in _ICOEI_ , 2019, pp. 292–297. 

- [62] A. Ragav and G. K. Gudur, “Bayesian active learning for wearable stress and affect detection,” _arXiv preprint arXiv:2012.02702_ , 2020. 

- [63] M. D. Koslovsky, E. T. H´ebert, M. S. Businelle, and M. Vannucci, “A bayesian time-varying effect model for behavioral mhealth data,” _Ann Appl Stat_ , vol. 14, no. 4, p. 1878, 2020. 

- [64] P. W. Koh and P. Liang, “Understanding black-box predictions via influence functions,” in _ICML_ , 2017, pp. 1885–1894. 

- [65] B. Sharchilev, Y. Ustinovskiy, P. Serdyukov, and M. Rijke, “Finding influential training samples for gradient boosted decision trees,” in _ICML_ , 2018, pp. 4577–4585. 

- [66] K. Ogawa, Y. Suzuki, and I. Takeuchi, “Safe screening of non-support vectors in pathwise svm computation,” in _ICML_ , 2013, pp. 1382–1390. 

- [67] A. Kendall and Y. Gal, “What uncertainties do we need in bayesian deep learning for computer vision?” in _NeurIPS_ , 2017, pp. 5574–5584. 

**Zhenzhe Zheng** is an assistant professor in the Department of Computer Science and Engineering, Shanghai Jiao Tong University. He received the B.E. in Software Engineering from Xidian University, in 2012, and the M.S. degree and the Ph.D. degree in Computer Science and Engineering from Shanghai Jiao Tong University, in 2015 and 2018, respectively. He has visited the University of Illinois at UrbanaChampaign (UIUC) as a Post Doc Research Associate from 2018 to 2019. His research interests include game theory and mechanism design, networking and mobile computing, and online marketplaces. He is a recipient of the China Computer Federation (CCF) Excellent Doctoral Dissertation Award 2018, Google Ph.D. Fellowship 2015 and Microsoft Research Asia Ph.D. Fellowship 2015. He has served as the member of technical program committees of several academic conferences, such as MobiHoc, AAAI, MSN, IoTDI and etc. He is a member of the ACM, IEEE, and CCF. For more information, please visit https://zhengzhenzhe220.github.io/ 

- [68] A. Der Kiureghian and O. Ditlevsen, “Aleatory or epistemic? does it matter?” _Structural safety_ , vol. 31, no. 2, pp. 105–112, 2009. 

Authorized licensed use limited to: Shanghai Jiaotong University. Downloaded on October 18,2023 at 01:05:52 UTC from IEEE Xplore.  Restrictions apply. © 2023 IEEE. Personal use is permitted, but republication/redistribution requires IEEE permission.��See https://www.ieee.org/publications/rights/index.html for more information. 

This article has been accepted for publication in IEEE Transactions on Mobile Computing. This is the author's version which has not been fully edited and content may change prior to final publication. Citation information: DOI 10.1109/TMC.2023.3316145 

17 

IEEE TRANSACTION ON MOBILE COMPUTING, VOL. XXX, NO. XXX, XXX 


![](assets/TMC23/TMC23.pdf-0017-03.png)


**Qinya Li** received her B.S. degree in Computer Science and Engineering from Northeastern University, P.R.China in 2015, and the Ph.D. degree in Computer Science and Engineering from Shanghai Jiao Tong University in 2020. Her research interests include mobile computing, mobile crowdsourcing, and algorithmic game theory and its applications. 

**Fan Wu** is a professor in the Department of Computer Science and Engineering, Shanghai Jiao Tong University. He received his B.S. in Computer Science from Nanjing University in 2004, and Ph.D. in Computer Science and Engineering from the State University of New York at Buffalo in 2009. He has visited the University of Illinois at Urbana-Champaign (UIUC) as a Post Doc Research Associate. His research interests include wireless networking and mobile computing, data management, algorithmic network economics, and privacy preservation. He has published more than 200 peer-reviewed papers in technical journals and conference proceedings. He is a recipient of the first class prize for Natural Science Award of China Ministry of Education, China National Fund for Distinguished Young Scientists, ACM China Rising Star Award, CCFTencent “Rhinoceros bird” Outstanding Award, and CCF-Intel Young Faculty Researcher Program Award. He has served as an associate editor of IEEE Transactions on Mobile Computing and ACM Transactions on Sensor Networks, an area editor of Elsevier Computer Networks, and as the member of technical program committees of more than 100 academic conferences. For more information, please visit http://www.cs.sjtu.edu.cn/�fwu/. 

**Guihai Chen** earned his B.S. degree from Nanjing University in 1984, M.E. degree from Southeast University in 1987, and Ph.D. degree from the University of Hong Kong in 1997. He is a distinguished professor of Shanghai Jiao Tong University, China. He had been invited as a visiting professor by many universities including Kyushu Institute of Technology, Japan in 1998, University of Queensland, Australia in 2000, and Wayne State University, USA during September 2001 to August 2003. He has a wide range of research interests with focus on sensor networks, peer-topeer computing, high-performance computer architecture and combinatorics. He has published more than 200 peer-reviewed papers, and more than 120 of them are in well-archived international journals such as IEEE Transactions on Parallel and Distributed Systems, Journal of Parallel and Distributed Computing, Wireless Networks, The Computer Journal, International Journal of Foundations of Computer Science, and Performance Evaluation, and also in well-known conference proceedings such as HPCA, MOBIHOC, INFOCOM, ICNP, ICPP, IPDPS and ICDCS. 

Authorized licensed use limited to: Shanghai Jiaotong University. Downloaded on October 18,2023 at 01:05:52 UTC from IEEE Xplore.  Restrictions apply. © 2023 IEEE. Personal use is permitted, but republication/redistribution requires IEEE permission.��See https://www.ieee.org/publications/rights/index.html for more information. 

