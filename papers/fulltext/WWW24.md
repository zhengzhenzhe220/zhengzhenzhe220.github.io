---
source: WWW24.pdf
pages: 11
converter: pymupdf4llm
converted_at: 2026-08-30T22:14:13+08:00
---


![](assets/WWW24/WWW24.pdf-0001-00.png)


# **Trajectory-wise Iterative Reinforcement Learning Framework for Auto-bidding** 

Haoming Li<sup>∗</sup> Yusen Huo Shuai Dou Shanghai Jiao Tong University Alibaba Group Alibaba Group Shanghai, China Beijing, China Beijing, China wakkkka@sjtu.edu.cn huoyusen.huoyusen@alibabadoushuai.ds@alibaba-inc.com inc.com 

Zhenzhe Zheng<sup>†</sup> Zhilin Zhang Shanghai Jiao Tong University Alibaba Group Shanghai, China Beijing, China zhengzhenzhe@sjtu.edu.cn zhangzhilin.pt@alibaba-inc.com 

Chuan Yu Alibaba Group Beijing, China yuchuan.yc@alibaba-inc.com 

Fan Wu Shanghai Jiao Tong University Shanghai, China fwu@cs.sjtu.edu.cn 

Jian Xu Alibaba Group Beijing, China xiyu.xj@alibaba-inc.com 

## **CCS CONCEPTS** 

## **ABSTRACT** 

In online advertising, advertisers participate in ad auctions to acquire ad opportunities, often by utilizing auto-bidding tools provided by demand-side platforms (DSPs). The current auto-bidding algorithms typically employ reinforcement learning (RL). However, due to safety concerns, most RL-based auto-bidding policies are trained in simulation, leading to a performance degradation when deployed in online environments. To narrow this gap, we can deploy multiple auto-bidding agents in parallel to collect a large interaction dataset. Offline RL algorithms can then be utilized to train a new policy. The trained policy can subsequently be deployed for further data collection, resulting in an iterative training framework, which we refer to as iterative offline RL. In this work, we identify the performance bottleneck of this iterative offline RL framework, which originates from the ineffective exploration and exploitation caused by the inherent conservatism of offline RL algorithms. To overcome this bottleneck, we propose Trajectory-wise Exploration and Exploitation (TEE), which introduces a novel data collecting and data utilization method for iterative offline RL from a trajectory perspective. Furthermore, to ensure the safety of online exploration while preserving the dataset quality for TEE, we propose Safe Exploration by Adaptive Action Selection (SEAS). Both offline experiments and real-world experiments on Alibaba display advertising platform demonstrate the effectiveness of our proposed method. 

- **Information systems** → **Computational advertising** ; • **Com-** 

- **puting methodologies** → **Reinforcement learning** . 

## **KEYWORDS** 

Real-time bidding, Reinforcement Learning, Offline Reinforcement Learning 

### **ACM Reference Format:** 

Haoming Li, Yusen Huo, Shuai Dou, Zhenzhe Zheng, Zhilin Zhang, Chuan Yu, Jian Xu, and Fan Wu. 2024. Trajectory-wise Iterative Reinforcement Learning Framework for Auto-bidding. In _Proceedings of the ACM Web Conference 2024 (WWW ’24), May 13–17, 2024, Singapore, Singapore._ ACM, New York, NY, USA, 11 pages. https://doi.org/10.1145/3589334.3645534 

## **1 INTRODUCTION** 

Online advertising is becoming one of the major sources of profit for Internet companies [7]. Due to the complex online advertising environments, auto-bidding tools provided by demand-side platforms (DSPs) are commonly used to bid on behalf of advertisers to optimize their advertising performance. Bidding for arriving ad impressions can be viewed as a sequential decision-making problem, and thus state-of-the-art auto-bidding algorithms leverage reinforcement learning (RL) to optimize bidding policies [4, 12, 31]. 

However, due to safety concerns, current RL-based auto-bidding policies are trained in simulated environments. Policies trained with simulation are shown suboptimal when deployed in the real-world system [21]. Therefore, it is desirable to optimize the bidding policy by directly interacting with the online environments. Classical (online) RL algorithms iteratively switch between data collection phase and policy update phase, and typically require enormous samples (i.e., transition tuples) to achieve convergence. However, collecting data samples can be extremely time-consuming, _e.g._ , in most RL formulations for auto-bidding [12, 31], an RL episode corresponds to 24 hours, and thus training a policy may take a long 

∗Work done during internship at Alibaba Group. 

†Zhenzhe Zheng is the corresponding author. 

Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the full citation on the first page. Copyrights for components of this work owned by others than the author(s) must be honored. Abstracting with credit is permitted. To copy otherwise, or republish, to post on servers or to redistribute to lists, requires prior specific permission and/or a fee. Request permissions from permissions@acm.org. _WWW ’24, May 13–17, 2024, Singapore, Singapore_ 

© 2024 Copyright held by the owner/author(s). Publication rights licensed to ACM. ACM ISBN 979-8-4007-0171-9/24/05...$15.00 

https://doi.org/10.1145/3589334.3645534 

4193 

WWW ’24, May 13–17, 2024, Singapore, Singapore 

Haoming Li et al. 

time. Additionally, frequent updates of online policies may cause unstable performance and potentially risky bidding behaviours. 

To address these issues, DSPs usually leverage a large number of auto-bidding agents as parallel workers to allow for the efficient collection of large amount of interaction data, and train an autobidding policy on the dataset with offline RL [10, 18] — a datadriven RL paradigm that aim to extract policies from large-scale pre-collected datasets. The updated policy could again be deployed for further data collection, which results in an iterative framework for data collection and policy update. We refer to the above training paradigm as iterative offline RL, as depicted in Figure 1. Iterative offline RL presents a promising solution for online policy training in industrial scenarios, and similar ideas have also been mentioned in several academic works [20, 21, 35]. 

To facilitate effective policy improvement for each iteration in iterative offline RL, it is crucial for the collected datasets to encompass sufficient information regarding various states and actions. This requires the exploration policy to incorporate a degree of randomness, typically achieved by introducing noise perturbation to actions [19–21]. Nonetheless, employing a random exploration policy can adversely affect the performance of the trained policy. This is because the introduced randomness undermines the exploration policy’s performance, and offline RL algorithms heavily relies on the exploration policy due to the principle of conservatism (or pessimism) [9, 10, 15, 17, 27], which compels the newly updated policy to be close to the exploration policy. We demonstrate this phenomenon in Section 4, highlighting the challenges of effective exploration and exploitation for iterative offline RL. 

In this work, we tackle the aforementioned challenges by adopting a trajectory perspective for both the exploration process (data collection) and the exploitation process (offline RL training). For efficient exploration, we construct exploration policies by introducing noise into the policy’s parameter space instead of the traditional action space. This choice is motivated by our key observation that the injection of parameter space noise (PSN) yields an exploration dataset with a more dispersed trajectory return distribution (please refer to Section 5.1 for details). This observation indicates that the dataset contains a considerable number of high-return trajectories, which are valuable for offline training. For effective exploitation, we propose robust trajectory weighting to fully exploit high-return trajectories in the collected dataset. Specifically, instead of uniformly sampling the dataset during training, we assign high probability weights to high-return trajectories, thereby enhancing the impact of high-quality behaviours on the training process and overcoming the conservatism problem. However, the instability of online environments leads to highly random trajectory returns that often fail to reliably reflect the trajectory qualities. To address this issue, we design a new trajectory quality indicator by approximating the expectation of the stochastic rewards, enhancing the robustness of the trajectory weighting method. We leverage PSN for online exploration and utilize robust trajectory weighting to compute sampling probabilities before offline RL training, boosting the effectiveness of exploration and exploitation in iterative offline RL. 

Apart from effectiveness, safety constraints must also be taken into consideration during online exploration in real-world advertising systems. Random exploration can lead to risky bidding behaviours, negatively impacting the performance of advertisers. The 


![](assets/WWW24/WWW24.pdf-0002-07.png)


**Figure 1: Iterative offline RL with Trajectory-wise Exploration and Exploitation (TEE) and Safe Exploration by Adaptive Action Selection (SEAS). Components proposed in this work are highlighted in red.** 

safety of an exploration policy is captured by a performance lower bound, which ensures that the performance drop brought by exploration is acceptable. Ensuring safe exploration often requires imposing constraints on the original exploration policy. However, existing safety-guaranteeing methods [21] often lack awareness of action qualities. While they prevent dangerous behaviours, they also restrict some high-quality actions. This may hinder the emergence of high-return trajectories during exploration, and subsequently affect the performance of the training process. To preserve data quality while ensuring safety, we propose SEAS, which dynamically determines the safe exploration action at each time step based on the cumulative rewards up to that step, as well as the predicted future return. By making adaptive decisions, SEAS preserves the quality of the collected dataset to the fullest extent, and achieves theoretically guaranteed safety at the same time. 

The main contributions of this work are summarized as follows: 

- We identify and demonstrate that the performance bottleneck of the current iterative offline RL paradigm for autobidding algorithms mainly lies in ineffective exploration and exploitation caused by the conservatism principle of offline RL algorithms. 

- We propose TEE, a solution for effective exploration and exploitation in iterative offline RL for auto-bidding. TEE comprises two components: PSN for trajectory-wise exploration, and a novel Robust Trajectory Weighting algorithm for trajectory-wise exploitation. 

- For safe exploration in auto-bidding, we design SEAS, which adaptively decides the safe exploration action for each time step based on the cumulative rewards till that step. SEAS can guarantee provable safety and sacrifice minimal performance in policy learning when working together with TEE. 

- Extensive experiments in both simulated environments and Alibaba display advertising platform demonstrate the effectiveness of our solution in terms of trained policy’s performance, as well as the safety of the training process. 

4194 

WWW ’24, May 13–17, 2024, Singapore, Singapore 

Trajectory-wise Iterative Reinforcement Learning Framework for Auto-bidding 

## **2 RELATED WORK** 

_Reinforcement learning for auto-bidding._ Bid optimization in online advertising is a sequential decision procedure, and can be solved via reinforcement learning techniques. Cai et. al. [4] first formulated the auto-bidding problem as an MDP. Wu et. al. [31] and He et. al. [12] leveraged reinforcement learning to optimize bidding policies under various constraints. All of the above works train their RL bidding agent in a simulated environment. Mou et. al. [21] recognized the sim2real problem in auto-bidding, and designed an iterative offline RL framework to train the bidding policy online. 

_Offline RL._ Offline RL [10, 18, 26] (or batch RL) refers to the problem of policy optimization utilizing only previously collected data, without additional online interaction. Due to the distribution shift [10] problem that arises in offline RL, most algorithms conduct conservative policy learning, which compels the learning policy to stay close to the dataset. Various algorithms achieve this by directly regularizing the actor [9, 10, 16, 24], learning conservative value functions [17], or constraining the number of policy improvement steps [3, 15]. However, the conservatism principle causes the performance of trained policy to highly depend on the dataset quality. 

_Dataset coverage in offline RL._ Dataset coverage is a core factor that limits the performance of offline RL algorithms. Schweighofer et. al. [28] conducted extensive experiments to demonstrate that dataset coverage is essential for offline RL algorithms to learn a good policy. Prior theoretical works on offline RL [5, 27, 34] also relied on datasets with sufficient state-action space coverage, which is often characterized by concentrability coefficients, to produce a strong performance guarantee. 

_Exploration in RL._ Exploration is a crucial aspect of RL as it allows the agent to gather information about the environment. Traditional exploration strategies induce novel behaviours by random perturbations of actions, such as _𝜖_ -greedy [29] and entropy regularization [30]. To generate meaningful behavioural patterns for hard exploration tasks, several other approaches such as intrinsic reward-based exploration [6, 23], count-based exploration [2, 22] and PSN [8, 25] have been proposed. However, most of the existing solutions have been proposed for the online RL paradigm, which is substantially different from iterative offline RL where data is collected for training offline RL algorithms. 

The state _𝑠𝑡_ is a feature vector describing the advertising status of a campaign, which may contain time, remaining budget, budget consumption speed, and etc. The action _𝑎𝑡_ is the bidding parameter _𝜆_ in time step _𝑡_ . The reward _𝑟_ ( _𝑠𝑡 ,𝑎𝑡_ ) is the total value of impressions won between time step _𝑡_ and _𝑡_ + 1, and _𝑝_ ( _𝑠𝑡_ +1| _𝑠𝑡 ,𝑎𝑡_ ) denotes the transition probability of states. Both _𝑟_ and _𝑝_ are determined by the advertising environment. The discount factor _𝛾_ ∈[0 _,_ 1] accounts for the future rewards’ diminishing impact. A (deterministic) policy _𝜋_ ∈ Π : S →A is a function defining the agent’s bidding behaviour. When a policy interacts with the advertising environment over an episode, a trajectory _𝜏_ = {( _𝑠𝑡 ,𝑎𝑡 ,𝑠𝑡_ +1 _,𝑟𝑡_ )}<sup>_𝑇_</sup> _𝑡_ =0<sup>is generated1,</sup> where the initial state _𝑠_ 0 is drawn from a probability distribution _𝜌_ . The (discounted) return of trajectory _𝜏_ is _𝑅_ ( _𝜏_ ) =<sup>�</sup><sup>_𝑇_</sup> _𝑡_ =0<sup>_𝛾𝑡𝑟𝑡_. The</sup> objective of RL is to maximize the expected return: 


![](assets/WWW24/WWW24.pdf-0003-08.png)


In RL, the state value function of a policy _𝜋_ is defined as 


![](assets/WWW24/WWW24.pdf-0003-10.png)


Similarly, the action value function is 


![](assets/WWW24/WWW24.pdf-0003-12.png)


Iterative offline RL follows a cyclical pattern of data collection and offline policy update, repeatedly for a total of _𝐾_ iterations. Within each iteration _𝑘_ ∈[ _𝐾_ ], an exploration policy _𝜋𝑒_<sup>_𝑘_</sup> is constructed based on _𝜋_<sup>_𝑘_</sup> . Then _𝜋𝑒_<sup>_𝑘_</sup> is deployed in the advertising environment to collect interaction dataset _𝐷_<sup>_𝑘_</sup> = { _𝜏𝑖_ } _𝑖_<sup>_𝑁_</sup> =1<sup>containing</sup><sup>_𝑁_</sup> trajectories. An offline RL algorithm is then used to learn a policy from _𝐷_<sup>_𝑘_</sup> , producing the updated policy _𝜋_<sup>_𝑘_+1</sup> for the subsequent iteration. 

**Safety of Bidding Policies.** The performance of auto-bidding policies deployed in the advertising system must be guaranteed in either the stages of policy deployment or policy training. Therefore, safety of the RL training process is formally defined by a performance lower bound: 


![](assets/WWW24/WWW24.pdf-0003-15.png)


where _𝐽𝑠_ is the performance of a known safe policy.<sup>2</sup> 

## **3 PRELIMINARIES** 

In this work, we consider auto-bidding with budget constraint, a sequential decision problem, where an advertiser submits bids for incoming ad impressions, aiming to maximize the total value within a fixed budget. For this problem, previous works [36, 37] showed that under the second price auction [ **?** ], the optimal bid _𝑏_<sup>∗</sup> on an impression is given by _𝑏_<sup>∗</sup> = _𝑣_ / _𝜆_ , where _𝑣_ represents the impression value ( _e.g._ click-through rate) and _𝜆_ is a scaling factor. However, determining the optimal value of _𝜆_ in real time is intractable due to its dependence on values and costs of all impressions in the stream. Thus, we formulate the problem of adjusting bidding parameter _𝜆_ as a Markov Decision Process (MDP), defined by a tuple (S _,_ A _,𝑟, 𝑝,𝛾_ ). In our formulation, an episode corresponds to a one-day ad campaign duration, which is divided into _𝑇_ time steps. At each step _𝑡_ , the advertiser observes state _𝑠𝑡_ ∈S and takes an action _𝑎𝑡_ ∈A. 

## **4 PERFORMANCE BOTTLENECK OF ITERATIVE OFFLINE RL** 

In this section, we present empirical observations regarding the performance bottleneck of iterative offline RL, and also introduce the idea of our proposed method. In each iteration of iterative offline RL, the data-collection policy plays a crucial role in determining the input dataset for the subsequent offline training process, which in turn influences the trained policy. The data-collection process 

> 1For simplicity, we assume all trajectories’ lengths are equal to episode length _𝑇_ , though a campaign may exhaust its budget at certain time _𝑡_ 0 _< 𝑇_ and cannot afford any impression thereafter. In such cases, we let _𝑟_ ( _𝑠𝑡 ,𝑎𝑡_ ) = 0 _,_ ∀ _𝑡_ 0 ≤ _𝑡_ ≤ _𝑇_ . 

> 2Note that the exploration policy _𝜋𝑒𝑘_<sup>in every iteration</sup><sup>_𝑘_should be ensured to be safe.</sup> To satisfy the safety constraint in the first iteration, the training process should be initialized by a known safe (but could be suboptimal) policy instead of a random policy. In practice, policies trained in a simulation [12] could serve as an initial policy. 

4195 

WWW ’24, May 13–17, 2024, Singapore, Singapore 

Haoming Li et al. 


![](assets/WWW24/WWW24.pdf-0004-02.png)


**Figure 2: Performance of exploration policies with different noise scale, as well as the performance of policies trained with IQL on datasets collected by those exploration policies.** 


![](assets/WWW24/WWW24.pdf-0004-04.png)


**Figure 3: Comparison of trajectory return distributions of datasets collected by ASN and PSN.** 

employing PSN instead of ASN for exploration leads to a dataset containing more high-return trajectories. 

should gather sufficient information of the underlying MDP through effective exploration. 

A conventional approach for exploration in iterative offline RL [20] is adding noise perturbations to actions. Concretely, an exploration policy with action space noise (ASN) is constructed as _𝜋𝑒_<sup>_𝐴𝑆𝑁_</sup> ( _𝑠𝑡_ ) = _𝜋_ ( _𝑠𝑡_ ) + _𝜖𝑡_ , where _𝜖𝑡_ ∼N (0 _, 𝜎_<sup>2</sup> _𝐼_ ) is sampled from a Gaussian distribution with standard deviation _𝜎_ . However, a highly random policy often leads to suboptimal performance and results in a dataset consisting primarily of low-quality actions. Consequently, such datasets pose challenges for offline RL algorithms to produce high-quality policies in the subsequent training process. This is because the conservatism principle of these algorithms drives the learned policy close to the low-performing exploration policy. 

We conduct experiments in a simulated environment (details provided in Appendix D) to illustrate the aforementioned issue. Based on one deterministic policy, we construct exploration policies by adding different levels of noise perturbation on the actions. These exploration policies are deployed in the environment to collect interaction datasets, which are then utilized by IQL [15], an offline RL algorithm, to train new policies. Figure 2 presents the performance of exploration policies with varying noise scale, as well as performance of the trained policies. We can observe that adding a certain amount of noise boosts the trained policy by gaining more environment information, while an excessively noisy exploration policy undermines the training result. Furthermore, the optimal noise scale depends on the training algorithm, making online tuning of the noise scale impractical. 

One potential method for overcoming the difficulty brought by conservatism is to manually identify high-quality behaviours from the noisy dataset and allow the learning algorithm to focus solely on these behaviours. However, evaluating the quality of individual actions within a dataset can be challenging. For one transition tuple ( _𝑠,𝑎,𝑟,𝑠_<sup>′</sup> ), a large reward _𝑟_ does not necessarily indicate _𝑎_ to be a good action, due to the influence of _𝑠_<sup>′</sup> on future rewards. Hopefully, if a full trajectory _𝜏_ attains a high return, then it is reasonable to infer that this trajectory contains high-quality behaviours. In following sections, we present empirical findings to reveal that 

## **5 PROPOSED FRAMEWORK** 

In this section, we present our novel design on iterative offline RL framework for auto-bidding, which comprises two key components: TEE and SEAS. 

## **5.1 Trajectory-wise Exploration** 

We introduce Parameter Space Noise (PSN) [8, 25] for exploration in the iterative offline RL framework, and explain its effectiveness from a trajectory view. PSN refers to injecting noise in an RL policy’s parameter space in order to induce exploratory behaviours. It has brought performance gain on a wide range of control tasks when applied to online deep RL algorithms [1, 13]. For a parameterized policy ( _e.g._ a neural network) _𝜋_ ( _𝑠_ ; _𝜃_ ), where _𝜃_ is the parameter vector, applying additive Gaussian noise to _𝜃_ gives _𝜃_<sup>ˆ</sup> = _𝜃_ + _𝜖_ , where _𝜖_ ∼N (0 _, 𝜎_<sup>2</sup> _𝐼_ ). Then the exploration policy based on PSN is _𝜋𝑒_<sup>_𝑃𝑆𝑁_</sup> ( _𝑠𝑡_ ) = _𝜋_ ( _𝑠𝑡_ ; _𝜃_<sup>ˆ</sup> ). Importantly, the perturbed parameter vector _𝜃_ ˆ is only sampled at the beginning of each episode and remains fixed afterwards. This is substantially different from ASN where independent noise is added at every time step. 

We now present our key observation on datasets collected by PSN by experiments in a simulated bidding environment (details are provided in Appendix D). We first construct two exploration policies with ASN and PSN based on one policy _𝜋_ , and denote them by _𝜋𝑒_<sup>_𝐴𝑆𝑁_</sup> and _𝜋𝑒_<sup>_𝑃𝑆𝑁_</sup> respectively. Subsequently, two datasets _𝐷_<sup>_𝐴𝑆𝑁_</sup> and _𝐷_<sup>_𝑃𝑆𝑁_</sup> of equal size are collected with _𝜋𝑒_<sup>_𝐴𝑆𝑁_</sup> and _𝜋𝑒_<sup>_𝑃𝑆𝑁_</sup> .<sup>3</sup> As shown in Figure 3, the return distribution of trajectories in _𝐷_<sup>_𝑃𝑆𝑁_</sup> is more dispersed than that of _𝐷_<sup>_𝐴𝑆𝑁_</sup> . Specifically, _𝐷_<sup>_𝑃𝑆𝑁_</sup> contains high-return trajectories ( _e.g._ trajectories with return higher than 750) which are almost absent in _𝐷_<sup>_𝐴𝑆𝑁_</sup> . 

The high return variance observed in PSN can be attributed to two main factors: decoupling between the exploration policy and the base policy (i.e. the original noiseless policy _𝜋_ ), and the consistency of exploration behaviours. The following example provides 

> 3To ensure a fair comparison, we control the noise strength of both exploration policies to guarantee that the average return of _𝐷_<sup>_𝐴𝑆𝑁_</sup> and _𝐷_<sup>_𝑃𝑆𝑁_</sup> are equal. 

4196 

WWW ’24, May 13–17, 2024, Singapore, Singapore 

Trajectory-wise Iterative Reinforcement Learning Framework for Auto-bidding 

further explanation in the context of auto-bidding, by highlighting the incapability of ASN on generating high-return trajectories. Assume that the current policy _𝜋_ is suboptimal in that it produces relatively low bids across most states. In this case, positive perturbations _𝜖𝑡_ are desirable when applying ASN. However, when _𝜋𝑒_<sup>_𝐴𝑆𝑁_</sup> ( _𝑠𝑡_ ) is lifted, _𝜋_ ( _𝑠𝑡_ +1) would become low since the base policy _𝜋_ aims to maintain the smoothness of budget consumption, thereby offsetting the effect of high bid in step _𝑡_ . The counterbalancing actions of the base policy substantially prevent ASN from effectively exploring unknown areas. Another issue with ASN is that, since the perturbations _𝜖𝑡_ of different time steps are drawn from independent probability distributions, consistently realizing positive _𝜖𝑡_ throughout an entire episode is barely possible. 

PSN enables us to sample a variety of policy parameters, which could be distributed to a great number of advertising campaigns in a DSP to explore different bidding behaviours. These campaigns run in parallel and collect a large dataset covering a wide range of behaviours, thus achieving large-scale trajectory-wise exploration. 

## **5.2 Trajectory-wise Exploitation** 

While PSN-based exploration policies could effectively generate valuable high-return trajectories, their collected datasets still consist primarily of inferior trajectories, as depicted in Figure 3. Therefore, the trained policy’s performance is still limited by the inherent conservatism of offline RL. To alleviate this problem and fully exploit the dataset, we propose Robust Trajectory Weighting for trajectorywise exploitation. 

We consider a dataset containing multiple trajectories _𝐷_ = { _𝜏𝑖_ } _𝑖_<sup>_𝑁_</sup> =1<sup>,where</sup><sup>_𝜏𝑖_={(</sup><sup>_𝑠𝑖,𝑡,𝑎𝑖,𝑡,𝑠𝑖,𝑡_+1</sup><sup>_,𝑟𝑖,𝑡_)}</sup><sup>_𝑇_</sup> _𝑡_ =0<sup>.Inspiredby[14,32,</sup> 33], instead of uniform sampling, we assign large sample probabilities to well-performing trajectories during training. A straightforward way to realize this is to assign weight _𝑤𝑖_ for trajectory _𝜏𝑖_ based on its return _𝑅𝑖_ � _𝑅_ ( _𝜏𝑖_ ), as high return typically indicates good behaviours. Nonetheless, two main issues arise when applying return-based trajectory weighting in the auto-bidding task. Firstly, due to the instability of auction environments and user feedbacks, the reward function _𝑟_ ( _𝑠𝑡 ,𝑎𝑡_ ) is highly stochastic, thus a high return might not necessarily be achieved by a good policy, but rather a "lucky" trial that happens to obtain high rewards in most time steps. Secondly, trajectories within the dataset may come from different advertising campaigns, and the intrinsic characteristics of a campaign, such as its budget level and item category, also affect the trajectory return. Thus, directly comparing trajectories from different campaigns by their returns is unfair. 

We address the first issue by learning a reward model _𝑟_ ¯ on the dataset for predicting the expected reward of a state-action pair: 


![](assets/WWW24/WWW24.pdf-0005-08.png)


The reward model could be implemented by a neural network with the above loss function. Then the original stochastic rewards _𝑟𝑖,𝑡_ are replaced with their expectations _𝑟_ ¯ _𝑖,𝑡_ = _𝑟_ ¯( _𝑠𝑖,𝑡 ,𝑎𝑖,𝑡_ ) to calculate _𝑅_ ¯ _𝑖_ =<sup>�</sup><sup>_𝑇_</sup> _𝑡_ =0<sup>_𝛾𝑡𝑟_¯</sup><sup>_𝑖,𝑡_, producing more robust quality indicators.</sup> 

To deal with the second issue mentioned above, we regularize the trajectory returns by subtracting the value of the initial state of the trajectory, estimated as _𝑉_<sup>ˆ</sup> = arg min _𝑉_ � _𝑖𝑁_ =1<sup>(</sup><sup>_𝑉_(</sup><sup>_𝑠𝑖,_0) −</sup><sup>_𝑅_¯</sup><sup>_𝑖_)2. The</sup> 

**Algorithm 1** Safe Exploration by Adaptive Action Selection (SEAS) 

|1:|**Input:**Exploration policy_𝜋𝑒_,_𝑛_distinct safe policies{_𝜋_<sup>_𝑖_</sup>_𝑠_}<sup>_𝑛_</sup><br>_𝑖_=1<br>and their state-action value function {_𝑄_<sup>_𝜋𝑖_</sup><br>_𝑠_}<sup>_𝑛_</sup><br>_𝑖_=1 <sup>, safe perfor-</sup><br>mance _𝐽𝑠_and safety coefficient_𝜖_∈(0_,_1)|
|---|---|
|2: <br>3:|**Initialize:**Sample initial state_𝑠_0 ∼_𝜌_(_𝑠_),_𝑡𝑒𝑚𝑝_←1<br> **for**_𝑡_=0_,_1_,_· · · _,𝑇_**do**<br>|
|4:|_𝑎𝑒_←_𝜋𝑒_(_𝑠𝑡_)_,𝑎𝑠_←_𝜋_<sup>_𝑡𝑒𝑚𝑝_</sup><br>_𝑠_<br>(_𝑠𝑡_)<br><br><sup>_𝑡𝑒𝑚_</sup>|
|5:|_𝑡𝑒𝑚𝑝_←arg max_𝑖𝑄_<sup>_𝜋𝑖_</sup><br>_𝑠_(_𝑠𝑡,𝑎𝑒_),_𝑄𝑚𝑎𝑥_←_𝑄_<sup>_𝜋𝑝_</sup><br>_𝑠_<br>(_𝑠𝑡,𝑎𝑒_)<br>|
|6:|**if** <sup>�</sup><sup>_𝑡_−1</sup><br>_𝑢_=0 <sup>_𝑟𝑢_+</sup><sup>_𝑄𝑚𝑎𝑥_≥(1 −</sup><sup>_𝜖_)</sup><sup>_𝐽𝑠_</sup><sup>**then**</sup>|
|7:|_𝑎𝑡_←_𝑎𝑒_|
|8:|**else**|
|9:|_𝑎𝑡_←_𝑎𝑠_|
|10:|**end if**|
|11:<br>12:|Take action_𝑎𝑡_, observe_𝑟𝑡,𝑠𝑡_+1<br> **end for**|



initial state typically contains information ( _e.g._ the total budget) of the advertising campaign, therefore _𝑉_<sup>ˆ</sup> ( _𝑠𝑖,_ 0) provides estimation of the expected return of the campaign behind trajectory _𝑖_ . Our final indicator of trajectory quality is _𝐴_<sup>ˆ</sup> _𝑖_ : 


![](assets/WWW24/WWW24.pdf-0005-14.png)


The sample probability _𝑤𝑖,𝑡_ of transition tuple ( _𝑠𝑖,𝑡 ,𝑎𝑖,𝑡 ,𝑠𝑖,𝑡_ +1 _,𝑟𝑖,𝑡_ ) is computed according to _𝐴_<sup>ˆ</sup> _𝑖_ as follows: 


![](assets/WWW24/WWW24.pdf-0005-16.png)


where _𝛼_ ∈ R<sup>+</sup> is a temperature parameter, and the weights should be normalized to ensure<sup>�</sup> _𝑖_<sup>_𝑁_</sup> =1 � _𝑇𝑡_ =0<sup>_𝑤𝑖,𝑡_= 1.</sup> 

After computing weights for dataset _𝐷_ , we could run any modelfree offline RL algorithm ( _e.g._ CQL, IQL) using the reweighted data sampling strategy. We provide a theoretical justification of Robust Trajectory Weighting in Appendix A, showing how it alleviates the problem brought by conservative algorithms. 

## **5.3 Safe Exploration** 

Although TEE boosts the effectiveness of iterative offline RL, the safety of data-collecting policies, which is of great importance when training in real-world advertising systems, have not been considered. In this section, we propose a novel algorithm named SEAS to guarantee the safety of online exploration. 

On the problem of safe exploration in auto-bidding, Mou et. al. [21] designed a method based on safety zone, to restrict the exploratory actions around a safe policy. Specifically, _𝜋𝑒_ ( _𝑠𝑡_ ) ← _𝑐𝑙𝑖𝑝_ ( _𝜋𝑒_ ( _𝑠𝑡_ ) _, 𝜋𝑠_ ( _𝑠𝑡_ ) − _𝜉, 𝜋𝑠_ ( _𝑠𝑡_ ) + _𝜉_ ), where _𝜋𝑠_ is a known safe policy. Though this method is provably safe under some assumptions on the MDP, its safety heavily relies on the radius _𝜉_ which is intractable to determine. Besides, this approach lacks awareness of the quality of original exploration actions, and poses constraint on both bad and good actions, thus hurting the quality of collected datasets. SEAS mitigates these problems through an adaptive design. The aim of SEAS is to prevent the low-performing trajectories caused by the original exploration policy ( _e.g. 𝜋𝑒_<sup>_𝑃𝑆𝑁_</sup> ) to emerge, while preserving the high-quality ones to the fullest extent. 

The procedure of SEAS interacting with the environment for one episode is shown in Algorithm 1. In each step, SEAS selects 

4197 

WWW ’24, May 13–17, 2024, Singapore, Singapore 

Haoming Li et al. 

between an exploratory action _𝑎𝑒_ and a safe action _𝑎𝑠_ according to the condition in line 6. Note that multiple safe policies are provided to the algorithm, and in each step the safe policy with maximum Q value is chosen for constructing the condition. Utilizing multiple safe policies instead of one loosens the restriction in line 6, thus better preserving exploratory actions of _𝜋𝑒_ . The algorithm is "adaptive" in the sense that each action _𝑎𝑡_ depends on the rewards accumulated up to time _𝑡_ . 

The following theorem shows that SEAS theoretically guarantees safety for any exploration policy _𝜋𝑒_ . Proof of Theorem 1 is provided in Appendix B. 

Theorem 1. _For any policy 𝜋𝑒 and any 𝜖_ ∈(0 _,_ 1) _, given safe policies_ { _𝜋𝑠_<sup>_𝑖_</sup> }<sup>_𝑛_</sup> _𝑖_ =1<sup>_that satisfy 𝐽_(</sup><sup>_𝜋𝑖𝑠_)≥</sup><sup>_𝐽𝑠,_∀1≤</sup><sup>_𝑖_≤</sup><sup>_𝑛, the expected re-_</sup> _turn_ E _𝜏_ [ _𝑅_ ( _𝜏_ )] _of trajectories generated by SEAS satisfies_ E _𝜏_ [ _𝑅_ ( _𝜏_ )] ≥ (1 − _𝜖_ ) _𝐽𝑠 ._ 

The advantages of SEAS are summarized as follows: (i) SEAS needs only one hyperparameter _𝜖_ , which is in the definition of safety and is straightforward to set. (ii) The safety of SEAS is provable without additional assumptions on the underlying MDP. (iii) Experiments demonstrate that when functioning together with TEE, SEAS exhibits minimal performance sacrifice compared to baseline methods. 

TEE and SEAS together form an iterative RL framework for autobidding. Appendix C provides a detailed description of the overall procedure. 

## **6 EXPERIMENTS** 

We provide empirical evidence for the effectiveness of our approach by both simulated experiments and real-world experiments on Alibaba display advertising platform. 

## **6.1 Overall Performance in a Simulated Environment** 

A simulated advertising system is constructed for all the offline experiments in this work. Details of the setup and hyperparameters are provided in Appendix D. 

We test the effectiveness of TEE and SEAS by combining them with three different offline RL algorithms. We also implement three baselines: iterative versions of IQL with and without exploration, as well as SORL [21]. An expert policy is trained with TD3 [11], an online RL algorithm, to serve as a performance upper bound. Methods for comparison are listed below. 

- **TEE+SEAS+IQL [15] / CQL [17] / TD3BC [9].** Iterative offline RL with the proposed TEE and SEAS, using IQL / CQL / TD3BC as the offline RL algorithm. 

- **IterIQL+ASN.** Iterative offline RL using IQL as the offline RL algorithm. IQL is selected as a representative because it is the state-of-the-art model-free offline RL algorithm. Exploration policy _𝜋𝑒_<sup>_𝑘_</sup> is constructed by adding ASN on _𝜋_<sup>_𝑘_</sup> . 

- **IterIQL.** Iterative offline RL using IQL as the offline RL algorithm. No exploration noise is added, therefore _𝜋𝑒_<sup>_𝑘_</sup> = _𝜋_<sup>_𝑘_</sup> . 

- **SORL [21].** SORL follows the iterative offline RL framework. The authors proposed V-CQL for offline policy training and designed an SER policy for safe and efficient exploration. 


![](assets/WWW24/WWW24.pdf-0006-16.png)


**Figure 4: Overall performance in a simulated environment.** 


![](assets/WWW24/WWW24.pdf-0006-18.png)


**Figure 5: Safety constraint satisfaction.** 

**Evaluation Metrics.** We evaluate the performance of a policy in terms of expected return. Besides, we check the safety of exploration policy by comparing average return in the collected dataset with the safety threshold (1 − _𝜖_ ) _𝐽𝑠_ . 

Figure 4 presents the overall performance through iterations. Our proposed framework, combined with any of the three offline RL algorithms, substantially outperforms the baseline methods and achieves near-expert performance in approximately 5 iterations. Both Iterative IQL+ASN and SORL get stuck in suboptimal policies after limited performance improvements, suffering from the performance bottleneck we discussed in section 4. Additionally, Iterative IQL without exploration achieves barely any performance improvement, which demonstrates the necessity of exploration in iterative offline RL. 

4198 

WWW ’24, May 13–17, 2024, Singapore, Singapore 

Trajectory-wise Iterative Reinforcement Learning Framework for Auto-bidding 

**Table 1: Performance of our proposed method in real-world experiments.** 

|iteration|BuyCnt|ROI|CPA|ConBdg|GMV|
|---|---|---|---|---|---|
|1|+1.82%|+2.64%|-1.81%|-0.03%|+2.61%|
|2|+2.21%|+2.94%|-2.14%|+0.02%|+2.95%|
|3|+2.94%|+3.33%|-1.78%|+1.12%|+4.49%|
|4|+3.59%|+2.44%|-2.60%|+0.90%|+3.36%|



We present the performance of exploration policies during the training process in Figure 5. Combined with any offline RL algorithm, our framework consistently ensures the performance of exploration policies to be above the safety threshold (1 − _𝜖_ ) _𝐽𝑠_ , which validates the safety guarantee ability of SEAS. We also show the results when SEAS is omitted, in which the safety constraint is violated in early stages. 

## **6.2 Online Experiments** 

We conduct real-world experiments on Alibaba display advertising platform. In each iteration, we utilize 20000 advertising campaigns to collect data for an epsiode, and employ IQL for offline training. Each episode contains 48 time steps, which means that the bidding parameter is adjusted every 30 minutes. After each policy update, we conduct a 10-day online A/B test using 1500 campaigns. 

**Evaluation Metrics.** The return of the trained policy acts as our main metric of performance, and is referred to as BuyCnt in the online experiments. Additionally, we introduce several other metrics that are commonly used in the auto-bidding field. 

- **BuyCut.** The total value of ad impressions won by the advertiser. Our objective _𝐽_ in the RL formulation. 

- **ROI.** The ratio between the total revenue and the consumed budget of the advertiser. 

- **CPA.** Cost per aquisition, defined as the average cost for each successfully converted impression. A smaller CPA indicates a better performance of an auto-bidding policy. 

- **ConBdg.** The total consumed budget of the advertiser. 

- **GMV.** Gross Merchandise Volume, the total amount of sales over the campaign duration. 

Table 1 shows the performance of our method in each iteration, compared with a static baseline policy trained by CQL[17] on a pre-collected dataset. We can see that the BuyCnt of our policy improves steadily through iterations, and our method consistently outperforms the baseline across all metrics. 

## **6.3 Ablation Studies** 

We conduct ablation studies for a deeper analysis of the how different components work with each other in our method. Specifically, we aim to answer the following questions: (1) Do trajectory-wise exploration and trajectory-wise exploitation operate in close conjunction instead of being two independent components? (2) Does the reward model effectively reduce the influence of stochastic rewards in Robust Trajectory Weighting? (3) Does SEAS achieve the theoretical safety bound in practice? (4) While achieving the same 

safety bound, does SEAS sacrifices less performance than other baseline safety-guaranteeing methods? 

To answer these questions, we conduct extensive experiments in the simulated environment described in Section 6.1. 

**To answer Question 1.** We develop variants of TEE to delve deeper into how trajectory-wise exploration and trajectory-wise exploitation work together. We focus on one data-collection process followed by one offline training process. We omit SEAS in this experiment, to focus solely on TEE. An IQL policy is used as base policy _𝜋_ . Details of the variants are presented as follows. 

- **TEE** is implemented as described. 

- **w/o T-explore** removes trajectory-wise exploration (i.e. PSN). Instead, traditional ASN is used for _𝜋𝑒_ . To ensure a fair comparison, we control the strength of ASN to guarantee that the average return in _𝐷_ are equal to that of PSN. 

- **w/o T-exploit** removes trajectory-wise exploitation (i.e. Robust Trajectory Weighting). After collecting _𝐷_ by PSN, we train a new policy with uniform sampling. 

- **w/o TEE** removes TEE. ASN is used for exploration, and uniform sampling for training. 

Table 2 presents the performance of policies trained under different settings, and their performance gain over the base policy. We observe that TEE achieves significant performance improvement over the base policy under various budgets, while the absence of either component hurts its effectiveness. Interestingly, eliminating Trajectory-wise Exploitation leads to a substantial performance degradation. The reason behind this is that datasets collected by PSN contains a large fraction of undesirable actions, which are imitated by conservative algorithms. The above observation indicates that Trajectory-wise Exploration and Trajectory-wise Exploitation are inherently interconnected components, and their combination contributes substantially to the enhancement of the algorithm’s performance. 

**To answer Question 2.** We test the effectiveness of reward model in environments with different degrees of stochasticity. We first construct simulated environments with various stochasticity by controlling the variance of impression numbers per time step. In each environment, we collect an exploratory dataset with the same policy, and use two different data sampling strategies to train a policy on the dataset: a) Our proposed robust trajectory weighting. b) Trajectory weighting with the raw rewards _𝑟𝑖,𝑡_ instead of the reward model’s prediction _𝑟_ ¯ _𝑖,𝑡_ . We compare the performance of trained policies, to examine how reward model benefits the trajectory weighting method. 

The results of the experiments are shown in Figure 6a, where _𝑅𝑟𝑜𝑏𝑢𝑠𝑡_ denotes the return of policy trained with Robust Trajectory Weighting, _𝑅𝑟𝑎𝑤_ represents the return of policy trained with raw rewards, and _𝑅𝑏𝑎𝑠𝑒_ the return of the data-collecting policy. Figure 6b shows the probability distributions of the impression number, where _𝑈_ [ _𝑎,𝑏_ ] denotes a uniform distribution over [ _𝑎,𝑏_ ]. The red line in Figure 6a indicates that the reward model is increasingly useful as the stochasticity of the environment intensifies. Moreover, the blue bars in the figure exhibit values lower than 1 in high stochasticity instances, which reflects that raw stochastic rewards could be misleading signals for trajectory weighting. 

4199 

WWW ’24, May 13–17, 2024, Singapore, Singapore 

Haoming Li et al. 

**Table 2: Ablation study on TEE. The last column presents the performance improvement over base policy. Best performance of each column is marked as bolded.** 

|Ablation Settings|||Budget|||_#Improve_|
|---|---|---|---|---|---|---|
||1500|2000|2500|3000|avg||
|Base policy|448.39|514.89|580.18|657.96|550.36|-|
|TEE|**490.19**±**13.38**|**569.35**±**5.89**|**634.88**±**31.88**|671_._68±59_._69|**591.53**±**24.79**|**+7.48%**|
|w/o T-explore|431_._09±11_._4|520_._12±12_._05|594_._14±13_._46|663_._18±14_._97|552_._13±7_._68|+0.32%|
|w/o T-exploit|365_._53±10_._55|414_._21±29_._05|495_._89±39_._82|571_._24±51_._27|461_._72±29_._96|-16.10%|
|w/o TEE|414_._38±30_._74|515_._66±10_._35|607_._47±8_._91|**678.67**±**17.53**|554_._04±7_._13|+0.66%|




![](assets/WWW24/WWW24.pdf-0008-04.png)


<!-- Start of picture text -->
Degree # of Impr.<br>low 175<br>medium-low 𝑈 [144 , 206]<br>medium 𝑈 [113 , 237]<br>medium-high 𝑈 [82 , 268]<br>high 𝑈 [50 , 300]<br>(b) Settings of different en-<br>vironments.<br>(a) Improvements of policy performance.<br><!-- End of picture text -->

**Table 4: Different safety ensuring methods’ impact on performance of trained policy. The third column presents the performance improvement of trained policy over base policy.** 

|Safe Exploration Methods|Return|_#Improve_|
|---|---|---|
|No constraint|594_._25±18_._28|+15.16%|
|SEAS|**572.35**±**20.42**|**+10.92%**|
|Small noise|528_._07±19_._45|+2.34%|
|Fixed range|532_._91±6_._74|+3.28%|



**Figure 6: The effectiveness of reward model in environments with different degrees of stochasticity.** 

**Table 3: Safety-ensuring ability of SEAS.** 

|_𝜖_|0.4|0.3|0.2|0.1|0.05|0.01|
|---|---|---|---|---|---|---|
|1−_𝐽_(_𝜋_<sup>_𝑘_</sup>_𝑒_)/_𝐽𝑠_|0.202|0.137|0.039|-0.002|-0.004|-0.005|



- **Fixed range.** As proposed in [21], the safe exploratory action _𝑎𝑒_ is given by _𝑎𝑒_ ← _𝑐𝑙𝑖𝑝_ ( _𝜋𝑒_ ( _𝑠𝑡_ ) _, 𝜋𝑠_ ( _𝑠𝑡_ ) − _𝜉, 𝜋𝑠_ ( _𝑠𝑡_ ) + _𝜉_ ). The safe policy _𝜋𝑠_ is the same as that in SEAS, and _𝜉_ is set to 0 _._ 1. 

The results are presented in Table 4. We also show the result of not imposing any safety constraint, which is a performance upper bound. SEAS significantly outperforms the two baselines in terms of the average return of the trained policy. This observation suggests that the adaptive design of SEAS allows for minimal performance sacrifice. 

## **7 CONCLUSION** 

**To answer Question 3.** We fully evaluate the safety-ensuring ability of SEAS by setting different values of _𝜖_ and observe the rate of performance decrease 1 − _𝐽_ ( _𝜋𝑒_<sup>_𝑘_</sup> )/ _𝐽𝑠_ , where _𝜋𝑒_<sup>_𝑘_</sup> is the policy produced by SEAS. We expect the safety constraint 1− _𝐽_ ( _𝜋𝑒_<sup>_𝑘_</sup> )/ _𝐽𝑠_ ≤ _𝜖_ to be satisfied. In this experiment, we take a USCB [12] policy as the safe policy, and obtain its _𝑄_ function through fitting a dataset collected by itself. 

From Table 3, we observe that SEAS consistently satisfies the safety constraint over a wide range of input _𝜖_ . Interestingly, for small _𝜖_ values, the exploration policy generated by SEAS even outperforms the base policy. 

**To answer Question 4.** We compare SEAS with two baseline safety-ensuring methods in terms of performance sacrificing, while ensuring safety to the same degree ( _𝜖_ = 0 _._ 05). One USCB [12] policy is leveraged as the safe policy. In this experiment, we start from an IQL policy, preserve the design of TEE, and substitute SEAS with baselines presented below. Strength of PSN is _𝜎_ = 0 _._ 05. 

- **Small noise.** We limit the strength of PSN at a low level, by setting _𝜎_ = 0 _._ 01. 

In this work, we have presented a new iterative RL framework for auto-bidding from a trajectory perspective. We also pay particular attention on the safety of exploration in online advertisement systems, and propose SEAS for this issue. Through comprehensive experiments, our method has been shown to be effective, achieving superior results compared to other baselines. In future work, we plan to test the effectiveness of TEE in other fields such as recommender systems and healthcare, where online policy training is challenging but urgently needed. 

## **ACKNOWLEDGMENTS** 

This work was supported in part by National Key R&D Program of China (No. 2022ZD0119100), in part by China NSF grant No. 62322206, 62132018, 62025204, U2268204, 62272307, 62372296, 61972254, 61972252, in part by Alibaba Group through Alibaba Innovative Research Program. The opinions, findings, conclusions, and recommendations expressed in this paper are those of the authors and do not necessarily reflect the views of the funding agencies or the government. 

4200 

WWW ’24, May 13–17, 2024, Singapore, Singapore 

Trajectory-wise Iterative Reinforcement Learning Framework for Auto-bidding 

## **REFERENCES** 

- [1] Adrià Puigdomènech Badia, Bilal Piot, Steven Kapturowski, Pablo Sprechmann, Alex Vitvitskyi, Zhaohan Daniel Guo, and Charles Blundell. 2020. Agent57: Outperforming the atari human benchmark. In _International conference on machine learning_ . PMLR, 507–517. 

- [2] Marc Bellemare, Sriram Srinivasan, Georg Ostrovski, Tom Schaul, David Saxton, and Remi Munos. 2016. Unifying count-based exploration and intrinsic motivation. _Advances in neural information processing systems_ 29 (2016). 

- [3] David Brandfonbrener, Will Whitney, Rajesh Ranganath, and Joan Bruna. 2021. Offline rl without off-policy evaluation. _Advances in neural information processing systems_ 34 (2021), 4933–4946. 

- [4] Han Cai, Kan Ren, Weinan Zhang, Kleanthis Malialis, Jun Wang, Yong Yu, and Defeng Guo. 2017. Real-time bidding by reinforcement learning in display advertising. In _Proceedings of the tenth ACM international conference on web search and data mining_ . 661–670. 

- [5] Jinglin Chen and Nan Jiang. 2019. Information-Theoretic Considerations in Batch Reinforcement Learning. In _Proceedings of the 36th International Conference on Machine Learning (Proceedings of Machine Learning Research, Vol. 97)_ . PMLR, 1042–1051. https://proceedings.mlr.press/v97/chen19e.html 

- [6] Nuttapong Chentanez, Andrew Barto, and Satinder Singh. 2004. Intrinsically motivated reinforcement learning. _Advances in neural information processing systems_ 17 (2004). 

- [7] Benjamin Edelman, Michael Ostrovsky, and Michael Schwarz. 2007. Internet advertising and the generalized second-price auction: Selling billions of dollars worth of keywords. _American economic review_ 97, 1 (2007), 242–259. 

- [8] Meire Fortunato, Mohammad Gheshlaghi Azar, Bilal Piot, Jacob Menick, Matteo Hessel, Ian Osband, Alex Graves, Volodymyr Mnih, Rémi Munos, Demis Hassabis, Olivier Pietquin, Charles Blundell, and Shane Legg. 2018. Noisy Networks For Exploration. In _6th International Conference on Learning Representations, ICLR 2018, Vancouver, BC, Canada, April 30 - May 3, 2018, Conference Track Proceedings_ . 

- [9] Scott Fujimoto and Shixiang Shane Gu. 2021. A minimalist approach to offline reinforcement learning. _Advances in neural information processing systems_ 34 (2021), 20132–20145. 

- [10] Scott Fujimoto, David Meger, and Doina Precup. 2019. Off-policy deep reinforcement learning without exploration. In _International conference on machine learning_ . PMLR, 2052–2062. 

- [11] Scott Fujimoto, Herke van Hoof, and David Meger. 2018. Addressing Function Approximation Error in Actor-Critic Methods. In _Proceedings of the 35th International Conference on Machine Learning (Proceedings of Machine Learning Research, Vol. 80)_ , Jennifer Dy and Andreas Krause (Eds.). PMLR, 1587–1596. https://proceedings.mlr.press/v80/fujimoto18a.html 

- [12] Yue He, Xiujun Chen, Di Wu, Junwei Pan, Qing Tan, Chuan Yu, Jian Xu, and Xiaoqiang Zhu. 2021. A unified solution to constrained bidding in online display advertising. In _Proceedings of the 27th ACM SIGKDD Conference on Knowledge Discovery & Data Mining_ . 2993–3001. 

- [13] Matteo Hessel, Joseph Modayil, Hado Van Hasselt, Tom Schaul, Georg Ostrovski, Will Dabney, Dan Horgan, Bilal Piot, Mohammad Azar, and David Silver. 2018. Rainbow: Combining improvements in deep reinforcement learning. In _Proceedings of the AAAI conference on artificial intelligence_ , Vol. 32. 

- [14] Zhang-Wei Hong, Pulkit Agrawal, Remi Tachet des Combes, and Romain Laroche. 2023. Harnessing Mixed Offline Reinforcement Learning Datasets via Trajectory Weighting. In _The Eleventh International Conference on Learning Representations, ICLR 2023, Kigali, Rwanda, May 1-5, 2023_ . 

- [15] Ilya Kostrikov, Ashvin Nair, and Sergey Levine. 2021. Offline Reinforcement Learning with Implicit Q-Learning. In _International Conference on Learning Representations_ . 

- [16] Aviral Kumar, Justin Fu, Matthew Soh, George Tucker, and Sergey Levine. 2019. Stabilizing off-policy q-learning via bootstrapping error reduction. _Advances in Neural Information Processing Systems_ 32 (2019). 

- [17] Aviral Kumar, Aurick Zhou, George Tucker, and Sergey Levine. 2020. Conservative q-learning for offline reinforcement learning. _Advances in Neural Information Processing Systems_ 33 (2020), 1179–1191. 

- [18] Sergey Levine, Aviral Kumar, George Tucker, and Justin Fu. 2020. Offline reinforcement learning: Tutorial, review, and perspectives on open problems. _arXiv preprint arXiv:2005.01643_ (2020). 

- [19] Timothy P. Lillicrap, Jonathan J. Hunt, Alexander Pritzel, Nicolas Heess, Tom Erez, Yuval Tassa, David Silver, and Daan Wierstra. 2016. Continuous control with deep reinforcement learning. In _4th International Conference on Learning Representations, ICLR 2016, San Juan, Puerto Rico, May 2-4, 2016, Conference Track Proceedings_ , Yoshua Bengio and Yann LeCun (Eds.). 

- [20] Tatsuya Matsushima, Hiroki Furuta, Yutaka Matsuo, Ofir Nachum, and Shixiang Gu. 2021. Deployment-Efficient Reinforcement Learning via Model-Based Offline Optimization. In _9th International Conference on Learning Representations, ICLR 2021, Virtual Event, Austria, May 3-7, 2021_ . 

- [21] Zhiyu Mou, Yusen Huo, Rongquan Bai, Mingzhou Xie, Chuan Yu, Jian Xu, and Bo Zheng. 2022. Sustainable Online Reinforcement Learning for Auto-bidding. In _Advances in Neural Information Processing Systems 35: Annual Conference on_ 

   - _Neural Information Processing Systems 2022, NeurIPS 2022, New Orleans, LA, USA, November 28 - December 9, 2022_ . 

- [22] Georg Ostrovski, Marc G Bellemare, Aäron Oord, and Rémi Munos. 2017. Countbased exploration with neural density models. In _International conference on machine learning_ . PMLR, 2721–2730. 

- [23] Deepak Pathak, Pulkit Agrawal, Alexei A Efros, and Trevor Darrell. 2017. Curiosity-driven exploration by self-supervised prediction. In _International conference on machine learning_ . PMLR, 2778–2787. 

- [24] Xue Bin Peng, Aviral Kumar, Grace Zhang, and Sergey Levine. 2019. Advantageweighted regression: Simple and scalable off-policy reinforcement learning. _arXiv preprint arXiv:1910.00177_ (2019). 

- [25] Matthias Plappert, Rein Houthooft, Prafulla Dhariwal, Szymon Sidor, Richard Y. Chen, Xi Chen, Tamim Asfour, Pieter Abbeel, and Marcin Andrychowicz. 2018. Parameter Space Noise for Exploration. In _6th International Conference on Learning Representations, ICLR 2018, Vancouver, BC, Canada, April 30 - May 3, 2018, Conference Track Proceedings_ . 

- [26] Rafael Figueiredo Prudencio, Marcos ROA Maximo, and Esther Luna Colombini. 2023. A survey on offline reinforcement learning: Taxonomy, review, and open problems. _IEEE Transactions on Neural Networks and Learning Systems_ (2023). 

- [27] Paria Rashidinejad, Banghua Zhu, Cong Ma, Jiantao Jiao, and Stuart Russell. 2021. Bridging offline reinforcement learning and imitation learning: A tale of pessimism. _Advances in Neural Information Processing Systems_ 34 (2021), 11702–11716. 

- [28] Kajetan Schweighofer, Marius-constantin Dinu, Andreas Radler, Markus Hofmarcher, Vihang Prakash Patil, Angela Bitto-Nemling, Hamid Eghbal-zadeh, and Sepp Hochreiter. 2022. A dataset perspective on offline reinforcement learning. In _Conference on Lifelong Learning Agents_ . PMLR, 470–517. 

- [29] Richard S Sutton and Andrew G Barto. 2018. _Reinforcement learning: An introduction_ . MIT press. 

- [30] Ronald J Williams. 1992. Simple statistical gradient-following algorithms for connectionist reinforcement learning. _Machine learning_ 8 (1992), 229–256. 

- [31] Di Wu, Xiujun Chen, Xun Yang, Hao Wang, Qing Tan, Xiaoxun Zhang, Jian Xu, and Kun Gai. 2018. Budget constrained bidding by model-free reinforcement learning in display advertising. In _Proceedings of the 27th ACM International Conference on Information and Knowledge Management_ . 1443–1451. 

- [32] Yang Yue, Bingyi Kang, Xiao Ma, Gao Huang, Shiji Song, and Shuicheng Yan. 2023. Offline Prioritized Experience Replay. _arXiv preprint arXiv:2306.05412_ (2023). 

- [33] Yang Yue, Bingyi Kang, Xiao Ma, Zhongwen Xu, Gao Huang, and Shuicheng Yan. 2022. Boosting offline reinforcement learning via data rebalancing. _arXiv preprint arXiv:2210.09241_ (2022). 

- [34] Wenhao Zhan, Baihe Huang, Audrey Huang, Nan Jiang, and Jason Lee. 2022. Offline Reinforcement Learning with Realizability and Single-policy Concentrability. In _Proceedings of Thirty Fifth Conference on Learning Theory (Proceedings of Machine Learning Research, Vol. 178)_ , Po-Ling Loh and Maxim Raginsky (Eds.). PMLR, 2730–2775. https://proceedings.mlr.press/v178/zhan22a.html 

- [35] Ruiyi Zhang, Tong Yu, Yilin Shen, and Hongxia Jin. 2022. Text-Based Interactive Recommendation via Offline Reinforcement Learning. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , Vol. 36. 11694–11702. 

- [36] Weinan Zhang, Kan Ren, and Jun Wang. 2016. Optimal real-time bidding frameworks discussion. _arXiv preprint arXiv:1602.01007_ (2016). 

- [37] Weinan Zhang, Shuai Yuan, and Jun Wang. 2014. Optimal real-time bidding for display advertising. In _Proceedings of the 20th ACM SIGKDD international conference on Knowledge discovery and data mining_ . 1077–1086. 

## **A THEORETICAL JUSTIFICATION OF ROBUST TRAJECTORY WEIGHTING** 

We formally show that under the assumption of deterministic transition and stochastic reward, applying Robust Trajectory Weighting is equivalent to training offline RL on a dataset collected by a better behaviour policy. 

For a dataset _𝐷_ = { _𝜏𝑖_ } _𝑖_<sup>_𝑁_</sup> =1<sup>where</sup><sup>_𝜏𝑖_={(</sup><sup>_𝑠𝑖,𝑡,𝑎𝑖,𝑡,𝑠𝑖,𝑡_+1</sup><sup>_,𝑟𝑖,𝑡_)}</sup><sup>_𝑇_</sup> _𝑡_ =0<sup>.</sup> Each trajectory _𝜏𝑖_ is collected by a different deterministic policy _𝜋𝑖_ , as in the case of Trajectory-wise Exploration. The behaviour policy _𝜋_ of _𝐷_ is then defined as sampling a policy from { _𝜋𝑖_ } _𝑖_<sup>_𝑁_</sup> =1 uniformly at the start of an episode, then acting according to the sampled policy till the end of the episode. Similarly, we define a weighted behaviour policy _𝜋_<sup>′</sup> as first sampling a policy from { _𝜋𝑖_ } _𝑖_<sup>_𝑁_</sup> =1 according to probabilities { _𝑤𝑖_ } _𝑖_<sup>_𝑁_</sup> =1<sup>, then acting with it. We aim to</sup> show that _𝐽_ ( _𝜋_<sup>′</sup> ) ≥ _𝐽_ ( _𝜋_ ). 

4201 

WWW ’24, May 13–17, 2024, Singapore, Singapore 

Haoming Li et al. 

The performance _𝐽_ ( _𝜋_ ) could be expressed as expectation of value function over all possible initial states: 

Proof. In each time step, SEAS takes either action _𝑎𝑒_ or _𝑎𝑠_ . For a trajectory _𝜏_ generated by SEAS, let _𝑡_ 0 be the last step it takes exploratory action _𝑎𝑒_ . For those trajectories where it never takes _𝑎𝑒_ , set _𝑡_ 0 to 0. Let _𝑡𝑒𝑚𝑝𝑡_ 0 denote the value of _𝑡𝑒𝑚𝑝_ at step _𝑡_ 0. Let 1( _𝜏,𝑠,𝑎,𝑖_ ) be the indicator function of _𝑠𝑡_ 0 _,𝑎𝑡_ 0 and _𝑡𝑒𝑚𝑝𝑡_ 0 for trajectory _𝜏_ , defined as follows: 


![](assets/WWW24/WWW24.pdf-0010-04.png)


For any initial state _𝑠_ 0, let _𝐺𝑠_ 0 = { _𝑖_ | _𝑠𝑖,_ 0 = _𝑠_ 0}, _𝑁𝑠_ 0 = | _𝐺𝑠_ 0 |, we have 


![](assets/WWW24/WWW24.pdf-0010-06.png)



![](assets/WWW24/WWW24.pdf-0010-07.png)



![](assets/WWW24/WWW24.pdf-0010-08.png)


where _𝛿_ (·) is the Dirac delta function. Therefore 


![](assets/WWW24/WWW24.pdf-0010-10.png)



![](assets/WWW24/WWW24.pdf-0010-11.png)


Assuming deterministic transition and stochastic rewards of the underlying MDP, we have _𝑉_<sup>_𝜋𝑖_</sup> ( _𝑠𝑖,_ 0) = _𝑅_<sup>¯</sup> _𝑖_ , where _𝑅_<sup>¯</sup> _𝑖_ =<sup>�</sup><sup>_𝑇_</sup> _𝑡_ =0<sup>_𝛾𝑡𝑟_¯</sup><sup>_𝑖,𝑡_is</sup> the relabeled return in Robust Trajectory Weighting. Plugging it in (2) and (3) gives us 

Multiply both sides of (10) by _𝑅_ ( _𝜏_ ), 


![](assets/WWW24/WWW24.pdf-0010-14.png)



![](assets/WWW24/WWW24.pdf-0010-15.png)


Take expectation with respect to _𝜏_ on both sides, 


![](assets/WWW24/WWW24.pdf-0010-17.png)


Split trajectory _𝜏_ by _𝑡_ 0, and define _𝑅_ ( _𝜏_<sup>−</sup> ) =<sup>�</sup> _𝑢_<sup>_𝑡_0</sup> =<sup>−</sup> 0<sup>1</sup><sup>_𝑟𝑢_,</sup><sup>_𝑅_(</sup><sup>_𝜏_+)=</sup> � _𝑇𝑢_ = _𝑡_ 0<sup>_𝑟𝑢_, then</sup> 

Subtracting (4) by (5), 


![](assets/WWW24/WWW24.pdf-0010-20.png)



![](assets/WWW24/WWW24.pdf-0010-21.png)


In (9), each term ( _𝑤𝑖_ − _𝑤 𝑗_ )( _𝑅_<sup>¯</sup> _𝑖_ − _𝑅_<sup>¯</sup> _𝑗_ ) inside the summation is non-negative, because 


![](assets/WWW24/WWW24.pdf-0010-23.png)


_𝑤𝑖_ = exp(( _𝑅_<sup>¯</sup> _𝑖_ / _𝑉_ ( _𝑠𝑖,_ 0) − 1)/ _𝛼_ )/ _𝑍,_ 

where _𝑍_ =<sup>�</sup> _𝑖_<sup>_𝑁_</sup> =1<sup>_𝑤𝑖_is a normalization term and</sup><sup>_𝛼_∈R+, is non-</sup> decreasing with respect to _𝑅_<sup>¯</sup> _𝑖_ . Therefore, _𝑉_<sup>_𝜋_′</sup> ( _𝑠_ 0) − _𝑉_<sup>_𝜋_</sup> ( _𝑠_ 0) ≥ 0 for every initial state _𝑠_ 0. Then applying (1) gives _𝐽_ ( _𝜋_<sup>′</sup> ) ≥ _𝐽_ ( _𝜋_ ). 

The above derivation also highlights the significance of our proposed reward model. Relabeling rewards with the reward model’s output makes _𝑉_<sup>_𝜋𝑖_</sup> ( _𝑠𝑖,_ 0) = _𝑅_<sup>¯</sup> _𝑖_ , allowing us to deal with stochastic rewards. 

## **B PROOF OF THEOREM 1** 

Theorem 1. _For any policy 𝜋𝑒 and any 𝜖_ ∈(0 _,_ 1) _, given safe policies_ { _𝜋𝑠_<sup>_𝑖_</sup> }<sup>_𝑛_</sup> _𝑖_ =1<sup>_that satisfy 𝐽_(</sup><sup>_𝜋𝑖𝑠_)≥</sup><sup>_𝐽𝑠,_∀1≤</sup><sup>_𝑖_≤</sup><sup>_𝑛, the expected re-_</sup> _turn_ E _𝜏_ [ _𝑅_ ( _𝜏_ )] _of trajectories generated by SEAS satisfies_ E _𝜏_ [ _𝑅_ ( _𝜏_ )] ≥ (1 − _𝜖_ ) _𝐽𝑠 ._ 

where the inequality step is by line 6 in algorithm 1, and the following steps are from (10) and simple algebra. □ 

4202 

WWW ’24, May 13–17, 2024, Singapore, Singapore 

Trajectory-wise Iterative Reinforcement Learning Framework for Auto-bidding 

## **C OVERALL ITERATIVE FRAMEWORK** 

TEE and SEAS are combined to form an iterative framework for online policy training in auto-bidding. The training process is initialized with the current policy running in the bidding system, which is typically suboptimal but safe. In each iteration _𝑘_ , we employ PSN for exploration based on the current policy _𝜋_<sup>_𝑘_</sup> . We pick a large number of advertising campaigns, and independently sample parameter vectors for different campaigns’ policies. The exploration policies are input to SEAS to guarantee safety. A subset of previous policies { _𝜋_<sup>_𝜅_</sup> } _𝜅_<sup>_𝑘_</sup> =<sup>−</sup> 1<sup>1can be utilized as safe policies for SEAS, and</sup><sup>_𝜖_is</sup> a pre-defined constant parameter through iterations. The Q functions of safe policies for SEAS could be obtained through different approaches. For policies trained by value-based or actor-critic RL algorithms, we can directly query the existing value network. Alternatively, new value networks can be fitted on the collected datasets. Specifically, for approximating the Q function of _𝜋_<sup>_𝜅_</sup> , we can perform SARSA-style policy evaluation on dataset _𝐷_<sup>_𝜅_</sup> . Although this yields underestimated values due to exploration when collecting _𝐷_<sup>_𝜅_</sup> , it does not incur violation of the safety constraint, because Theorem 1 still holds even when the input Q functions have underestimated values. The safe exploration policies are then distributed and deployed to multiple advertising campaigns, running in parallel for a specific duration ( _e.g._ one day) to collect an interaction dataset _𝐷_<sup>_𝑘_</sup> . Subsequently, we employ an offline RL algorithm ( _e.g._ IQL) to perform policy training on _𝐷_<sup>_𝑘_</sup> , where the sampling probabilities are computed using Robust Trajectory Weighting. The resulting trained policy _𝜋_<sup>_𝑘_+1</sup> becomes the input for the subsequent iteration, and the process continues iteratively. 

## **D DETAILS OF OFFLINE EXPERIMENTS** 

**Setup.** For offline experiments, we construct a simulated advertising system mainly based on the simulated system in [21]. There are 

30 advertisers competing for advertising impressions. An episode corresponds to one day in simulation, which is divided into 96 time steps. The number of impressions in each time step is random, and follows a uniform distribution on [50, 300]. The budget of each advertiser follows a uniform distribution on [1500, 3000]. Before an episode starts, the number of impressions in every time step, as well as the value of each impression for each advertiser is initialized. The state of an advertiser is three-dimensional: 

[ _𝑡𝑖𝑚𝑒,𝑏𝑢𝑑𝑔𝑒𝑡_  𝑐𝑜𝑛𝑠𝑢𝑚𝑒𝑑,𝑏𝑢𝑑𝑔𝑒𝑡_  𝑙𝑒𝑓𝑡_ ]. The reward of an advertiser is the total value she wins in all ad auctions during one time step. Given current states and actions of all advertisers, the simulation returns next states and rewards. This is achieved by simulating ad auctions for all impressions in a single time step. For each impression, the system performs pre-ranking and ranking, and decides the winner of the auction. The winner gets the value of the impression, and pays for it according to the auction mechanism. We train a bidding policy for one advertiser while keeping other 29 advertisers’ policy fixed. Therefore, the policies of other bidders could be seen as part of the environment which is stationary. The trained auto-bidding policy could serve for bidders with different budgets since the information of total budget is contained in the state representation. The implementation of the pre-ranking and ranking(auction) part follows from that in [21], where more details could be found. 

**Parameter Settings.** Datasets collected in each iteration consists of 100000 transition tuples. Strength of trajectory weighting _𝛼_ is set to 0.1. Safety threshold _𝜖_ is 0.05. PSN is implemented as factorised Gaussian noise [8] with _𝜎_ searched from [0.01,0.03,0.05] and kept fixed during training. ASN is Gaussian noise with _𝜎_ searched from [0.3,0.5,1]. In the IQL algorithm, the expectile parameter is set to 0.6 and _𝛽_ is 1.25. Conservative factor is chosen as _𝛼_ = 0 _._ 8 in CQL, and _𝛼_ = 2 _._ 5 in TD3+BC. Implementation of SORL is consistent with the original paper [21] and code. 

4203 

