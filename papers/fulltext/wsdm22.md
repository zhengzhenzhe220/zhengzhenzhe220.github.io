---
source: wsdm22.pdf
pages: 11
converter: pymupdf4llm
converted_at: 2026-08-30T22:11:48+08:00
---

# **A Cooperative-Competitive Multi-Agent Framework for Auto-bidding in Online Advertising** 

Chao Wen<sup>1</sup><sup>_,_3∗</sup> , Miao Xu<sup>3</sup> , Zhilin Zhang<sup>3</sup> , Zhenzhe Zheng<sup>2†</sup> , 

Yuhui Wang<sup>1</sup> , Xiangyu Liu<sup>3</sup> , Yu Rong<sup>3</sup> Dong Xie<sup>3</sup> , Xiaoyang Tan<sup>1</sup> , Chuan Yu<sup>3</sup> , Jian Xu<sup>3</sup> , Fan Wu<sup>2</sup> , Guihai Chen<sup>2</sup> , Xiaoqiang Zhu<sup>3</sup> and Bo Zheng<sup>3</sup> 

1MIIT Key Laboratory of Pattern Analysis and Machine Intelligence, China 

2Shanghai Jiao Tong University, China, 3Alibaba Group, China 

1{chaowen, y.wang, x.tan}@nuaa.edu.cn, 2{zhengzhenzhe@, fwu@cs., gchen@cs.}sjtu.edu.cn, 

3{xumiao.xm, zhangzhilin.pt, qilin.lxy, homer.ry robber.xd, yuchuan.yc, xiyu.xj, xiaoqiang.zxq, 

bozheng}@alibaba-inc.com 

## **ABSTRACT** 

In online advertising, auto-bidding has become an essential tool for advertisers to optimize their preferred ad performance metrics by simply expressing high-level campaign objectives and constraints. Previous works designed auto-bidding tools from the view of singleagent, without modeling the mutual influence between agents. In this paper, we instead consider this problem from a distributed multi-agent perspective, and propose a general <u>Multi-Agent rein-</u> forcement learning framework for <u>Auto-Bidding, namely MAAB,</u> to learn the auto-bidding strategies. First, we investigate the competition and cooperation relation among auto-bidding agents, and propose a temperature-regularized credit assignment to establish a mixed cooperative-competitive paradigm. By carefully making a competition and cooperation trade-off among agents, we can reach an equilibrium state that guarantees not only individual advertiser’s utility but also the system performance (i.e., social welfare). Second, to avoid the potential collusion behaviors of bidding low prices underlying the cooperation, we further propose bar agents to set a personalized bidding bar for each agent, and then alleviate the revenue degradation due to the cooperation. Third, to deploy MAAB in the large-scale advertising system with millions of advertisers, we propose a mean-field approach. By grouping advertisers with the same objective as a mean auto-bidding agent, the interactions among the large-scale advertisers are greatly simplified, making it practical to train MAAB efficiently. Extensive experiments on the 

This work was supported in part by Science and Technology Innovation 2030 – “New Generation Artificial Intelligence” Major Project No. 2018AAA0100905, China NSF grant No. 61902248, 61976115, in part by Shanghai Science and Technology Fund 20PJ1407900, in part by Alibaba Group through Alibaba Innovation Research Program and Alibaba Research Intern Program. The opinions, findings, conclusions, and recommendations expressed in this paper are those of the authors and do not necessarily reflect the views of the funding agencies or the government. ∗Work done during an internship at Alibaba Group. †Corresponding author. 

Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the full citation on the first page. Copyrights for components of this work owned by others than ACM must be honored. Abstracting with credit is permitted. To copy otherwise, or republish, to post on servers or to redistribute to lists, requires prior specific permission and/or a fee. Request permissions from permissions@acm.org. _WSDM ’22, February 21–25, 2022, Tempe, AZ, USA._ © 2022 Association for Computing Machinery. ACM ISBN 978-1-4503-9132-0/22/02...$15.00 https://doi.org/10.1145/3488560.3498373 

offline industrial dataset and Alibaba advertising platform demonstrate that our approach outperforms several baseline methods in terms of social welfare and revenue. 

## **CCS CONCEPTS** 

- **Information systems** → **Computational advertising** . 

## **KEYWORDS** 

Auto-bidding; Bid Optimization; Multi-Agent Reinforcement Learning; E-commerce Advertising 

#### **ACM Reference Format:** 

Chao Wen, Miao Xu, Zhilin Zhang, Zhenzhe Zheng, Yuhui Wang, Xiangyu Liu, Yu Rong, Dong Xie, Xiaoyang Tan, Chuan Yu, Jian Xu, Fan Wu, Guihai Chen, Xiaoqiang Zhu and Bo Zheng. 2022. A Cooperative-Competitive MultiAgent Framework for Auto-bidding in Online Advertising. In _Proceedings of the Fifteenth ACM International Conference on Web Search and Data Mining (WSDM ’22), February 21–25, 2022, Tempe, AZ, USA._ ACM, New York, NY, USA, 11 pages. https://doi.org/10.1145/3488560.3498373 

## **1 INTRODUCTION** 

In recent years, online advertising has become ubiquitous in modern advertising markets, and generates hundreds of billions of dollars every year [7]. Online advertising allows advertisers to increase the exposure opportunities of their products to potential audiences. Traditionally, advertisers need to manually adjust a bid in each ad auction to optimize the overall ad campaign performance. However, this fine-grained bidding process requires domain knowledge and comprehensive information about advertising environments [32]. To reduce the burden on bid optimization for advertisers, online platforms have deployed various types of auto-bidding services, such as Google’s AdWords campaign management tool [10] and Facebook’s automated bidding services [8]. These services allow advertisers to simply express high-level campaign objectives and constraints, and the auto-bidding agents would calculate the bids for each auction on behalf of advertisers to optimize their preferred ad performance metrics [3]. 

We illustrate the procedure of auto-bidding services for online advertising in Figure 1. The advertising platform designs auto-bidding agents, each of which learns a bidding strategy for the advertiser to optimize her desired objective under certain constraints. For example, in Alibaba advertising platform, there exist three typical types of auto-bidding agents: CLICK Agent, CONV Agent, and 


![](assets/wsdm22/wsdm22.pdf-0002-00.png)


**Figure 1: An Overview of Auto-bidding Services.** 

CART Agent, which optimize the number of clicks, purchase conversions and add-to-carts under budget constraints, respectively. These auto-bidding agents compete with each other by bidding for each ad display opportunity ( _impression opportunity_ ). After receiving an impression opportunity, the platform launches an ad auction for the participating auto-bidding agents, each of which places a bid according to the advertiser’s objective and constraint, as well as the predicted value ( _e.g._ , pCTR, pCVR or pCART) of this impression opportunity. After collecting bids from all the agents, the auction mechanism determines the winning advertisers and the corresponding payments. 

To learn the bidding strategies for auto-bidding agents, a natural option, also widely adopted in real-time-bidding (RTB) literature [1, 31], is to solve an isolated optimization problem for each auto-bidding agent, and the effects of other agents are implicitly encoded within the auction environment. However, this formulation ignores the fact that the ad auction mechanism is inherently a distributed multi-agent system in nature – the outcome of an ad auction depends heavily on the bidding behaviors of all the involved auto-bidding agents [14]. Without appropriate coordination, the auto-bidding agents would lead to an anarchy state with significantly degraded system performance, such as the _tragedy of the commons_ [12]. Thus, we leverage a distributed multi-agent framework associated with a carefully designed coordinated scheme to steer the behaviors of auto-bidding agents towards an equilibrium state with good system performance. 

There are still several challenges in designing the bidding strategies for auto-bidding agents under this framework [3, 32]. First, the complex competition and cooperation relations among auto-bidding agents hinder the platform to jointly optimize the individual agent’s utility and the overall system performance. On the one side, in a fully competitive multi-agent paradigm, each individual advertiser’s utility can be extremely optimized. For example, the auto-bidding agents with adequate budgets would bid aggressively and dominate a large number of ad auctions, for their own interests. However, the winning advertisers may contribute low social welfare, due to an inefficient ad allocation in a system-level view. On the other hand, a fully cooperative multi-agent scheme can resolve this issue as all the auto-bidding agents aim at maximizing the social welfare together, as in the centralized optimization. However, this method may sacrifice some advertisers’ utilities for a large social welfare, which is not healthy for the long-term prosperity of online advertising. We need to resolve the conflict between individual advertiser’s utility and the system performance (social welfare). A more proper way is 

to establish a mixed cooperative-competitive (MCC) framework, enabling the platform to make a flexible trade-off between individual utility and the system performance. Existing approaches to achieve this are through either manually modifying reward functions [27] or changing environment-related factors [16, 19]. However, there is still no specific reward function for auto-bidding agents in the context of ad auctions, and the environmental factors are only controllable in a simulator but not in the real-world online setting. 

Second, the cooperation in the MCC framework would inevitably reduce the platform’s revenue. This is because cooperative autobidding agents may collude with each other to bid low prices [20]. We can leverage the reserve price [22, 34], a classical method derived from the optimal auction theory [23], to boost the revenue of auction. However, the optimal reserve price is usually calculated in the non-cooperative auction setting with simple bidders/agents, and how to set the optimal reserve prices in the MCC framework that guarantees platform’s revenue without reducing social welfare is still unclear. 

The last but not least, the industrial deployment of a MCC multiagent framework for auto-bidding services is quite challenging. In a practical advertising platform, there are millions of advertisers competing for billions of impressions every day, thus it is difficult to formulate each advertiser as a single agent and train millions of agents simultaneously with limited computational resources and time. Besides, the sparsity of the rewards for each agent cannot properly direct the policy learning due to the limited impression opportunities with respective to the huge number of advertisers. 

By jointly considering the above design challenges, we propose a cooperative-competitive multi-agent reinforcement learning (MARL) framework for auto-bidding in online advertising, namely MAAB. First, to handle the trade-off between the cooperative and competitive relation among auto-bidding agents, we propose a temperature-regularized credit assignment scheme, which distributes the total reward from the auction among the participating agents in proportion to the weights captured by a softmax function. The temperature parameter in the softmax function could work as a controller to adjust the degree of the trade-off. Second, to reduce the loss of revenue, we design bar agents for learning a personalized bidding bar for each auto-bidding agent. Intuitively, the bar agent’s goal is to increase the bidding bar for a high revenue for the platform, while the auto-bidding agent has an opposite goal — reducing the bidding bar for a low payment. The bar agent’s training is implemented through an adversarial interaction with the training for auto-bidding agents until reaching some equilibrium point. Third, we propose a mean-field style approach [15, 33] to tackle the challenge from the industrial large-scale multi-agent system. By grouping the advertisers with the same objective as a mean auto-bidding agent, the complex interactions among millions of advertisers are significantly reduced to the interactions within a limited number of super auto-bidding agents, making it practical to train and deploy the large-scale multi-agent system for auto-bidding services. Extensive offline and online experiments demonstrate the effectiveness of our MAAB in terms of both social welfare and platform’s revenue.<sup>1</sup> 

The contributions in this paper can be summarized as follows: 

1Code is available at https://github.com/chaovven/maab. 

- (1) We investigated auto-bidding problem from the perspective of multi-agent systems, and proposed temperature-regularized credit assignment to properly model the mixed cooperativecompetitive relation among auto-bidding agents. 

- (2) We designed the bar agents to solve the multiple objectives in the cooperative-competitive auto-bidding framework, where platform’s revenue can be improved without reducing social welfare by adaptively setting the bidding bars. 

- (3) We proposed a mean-field style approach for handling the scalability of large-scale multi-agent system for auto-bidding. The evaluation results show the effectiveness of our method in terms of both social welfare and platform’s revenue. 

## **2 PRELIMINARIES** 

## **2.1 Auto-bidding Model** 

We consider the budget-constrained auto-bidding services, where advertisers hope to maximize the total value of winning impressions under a budget constraint [31]. The auto-bidding process is described as follows. During a period (e.g., one day) with _𝑇_ impression opportunities arriving sequentially, the auto-bidding agent gives the bid _𝑏𝑖_<sup>_𝑡_on behalf of advertiser</sup><sup>_𝑖_for the impression oppor-</sup> tunity arriving at timestep _𝑡_ . If _𝑏𝑖_<sup>_𝑡_is the highest bid in the auction,</sup> advertiser _𝑖_ displays her ad, obtains the impression value _𝑣𝑖_<sup>_𝑡_, and</sup> makes the payment _𝑝_<sup>_𝑡_</sup> , which is the second-highest bid in the second price auction. This bidding process terminates if the total payment reaches the budget limit or there are no impression opportunities left. The goal of auto-bidding agent that bids on behalf of advertiser _𝑖_ is to maximize the total value of winning impressions under the budget constraint: 


![](assets/wsdm22/wsdm22.pdf-0003-06.png)



![](assets/wsdm22/wsdm22.pdf-0003-07.png)


where _𝑥𝑖_<sup>_𝑡_∈{0</sup><sup>_,_1} denotes whether advertiser</sup><sup>_𝑖_wins the impression</sup> _𝑡_ . In the following discussion, we also use _𝑖_ to denote the autobidding agent of the advertiser _𝑖_ . 

## **2.2 Markov Games** 

The previous subsection describes auto-bidding services from the view of single-agent, we next use Markov Game [17] to model the interaction among multiple auto-bidding agents. We briefly recall the notations of Markov game. A partially observable Markov Game of _𝑛_ agents is a tuple consisting of _<_ S _, 𝑃,_ { _𝑍𝑖,_ O _𝑖,_ A _𝑖,𝑟𝑖_ }<sup>_𝑛_</sup> _𝑖_ =1<sup>_,𝛾>_.</sup> We use _𝑠_ ∈S to denote the state of the environment. At each timestep, each agent takes an action _𝑎𝑖_ = _𝜋𝑖_ ( _𝑜𝑖_ ) ∈A _𝑖_ according to its policy _𝜋𝑖_ and an observation _𝑜𝑖_ , drawing from the observation function _𝑍𝑖_ : S → _𝑂𝑖_ . After all the agents taking the joint action a = ( _𝑎_ 1 _,_ · · · _,𝑎𝑛_ ), each agent _𝑖_ obtains a scalar reward _𝑟𝑖_ : S × A1 × · · · × A _𝑛_ → R, and environment transits to the next state _𝑠_<sup>′</sup> according to the transition function _𝑃_ ( _𝑠_<sup>′</sup> | _𝑠,_ a) : S×A1 ×· · ·×A _𝑛_ → S. _𝛾_ ∈(0 _,_ 1] is a discount factor for future rewards. Each agent aims to learn its policy in order to maximize its expected accumulated reward _𝑅𝑖_ = E[<sup>�</sup><sup>_𝑇_</sup> _𝑡_ =1<sup>_𝛾𝑡_−1</sup><sup>_𝑟_</sup> _𝑖_<sup>_𝑡_]over the period.</sup> 

We describe the above Markov Game in the context of autobidding services. At each timestep _𝑡_ , an auto-bidding agent _𝑖_ decides the bid price _𝑏𝑖_<sup>_𝑡_=</sup><sup>_𝜋𝑖_(</sup><sup>_𝑜_</sup> _𝑖_<sup>_𝑡_)accordingtothereceivedobservation</sup> _𝑜𝑖_<sup>_𝑡_=(</sup><sup>_𝐵_</sup> _𝑖_<sup>_𝑡, 𝑣_</sup> _𝑖_<sup>_𝑡,𝑡𝑠_</sup> _𝑖_<sup>_𝑡_), where</sup><sup>_𝐵_</sup> _𝑖_<sup>_𝑡_is the remaining budget (the bid price is</sup> forced to be 0 when the remaining budget is 0), _𝑣𝑖_<sup>_𝑡_is the impression</sup> value and _𝑡𝑠𝑖_<sup>_𝑡_=</sup><sup>_𝑇_−</sup><sup>_𝑡_is the timesteps left. The reward for the winning</sup> auto-bidding agent is _𝑟𝑖_<sup>_𝑡_=</sup><sup>_𝑣_</sup> _𝑖_<sup>_𝑡_and the payment</sup><sup>_𝑝𝑡_is determined</sup> by the second-highest bid. After that, the environment transits to = the next state, and the new observation for each agent is _𝑜𝑖_<sup>_𝑡_+1</sup> ( _𝐵𝑖_<sup>_𝑡_−</sup><sup>_𝑝𝑡_×</sup><sup>_𝑥_</sup> _𝑖_<sup>_𝑡, 𝑣_</sup> _𝑖_<sup>_𝑡_+1</sup> _,𝑡𝑠𝑖_<sup>_𝑡_−1).Theobjective ofauto-biddingagent</sup> is to maximize its expected total value of winning impressions: max _𝜋𝑖_ E[<sup>�</sup><sup>_𝑇_</sup> _𝑡_ =1<sup>_𝛾𝑡_−1</sup><sup>_𝑟_</sup> _𝑖_<sup>_𝑡_].</sup> 

## **2.3 Independent Learner** 

The classical multi-agent reinforcement learning (MARL) algorithm for solving Markov Games is to directly learn decentralized value functions or policies simultaneously [27, 28]. Independent _𝑄_ -learning [27, 28] trains individual _𝑄_ function for each agent, with all agents sharing the same environment. We refer to independent _𝑄_ -learning as _independent learner (IL)_ . We represent each agent’s action-value function _𝑄𝑖_ ( _𝑜𝑖,𝑏𝑖_ ) that conditions on its observations and bids with a deep neural network parameterized by _𝜃𝑖_ ’s. A replay buffer D stores the transition tuple of all agents {( _𝑜𝑖,𝑏𝑖,𝑟𝑖,𝑜𝑖_<sup>′)}</sup><sup>_𝑛_</sup> _𝑖_ =1<sup>,</sup> where _𝑜𝑖_<sup>′is observed by agent</sup><sup>_𝑖_after submitting the bid</sup><sup>_𝑏𝑖_based</sup> on its observation _𝑜𝑖_ and receiving reward _𝑟𝑖_ . The training process of _𝑄𝑖_ ( _𝑜𝑖,𝑏𝑖_ ) is similar to DQN [21], where the parameters _𝜃𝑖_ ’s are learned by sampling batches of transitions from the replay memory, and minimizing the following loss function: 


![](assets/wsdm22/wsdm22.pdf-0003-14.png)


where the target _𝑦𝑖_ = _𝑟𝑖_<sup>train</sup> + _𝛾_ max _𝑏𝑖_<sup>′</sup><sup>_𝑄_(</sup><sup>_𝑜_</sup> _𝑖_<sup>′</sup><sup>_,𝑏_</sup> _𝑖_<sup>′;</sup><sup>_𝜃_ˆ</sup><sup>_𝑖_), and the tempo-</sup> rary parameters _𝜃_<sup>ˆ</sup> _𝑖_ ’s are periodically updated to the new _𝜃𝑖_ after a fixed number of timesteps. We use _𝑟𝑖_<sup>train</sup> to denote the reward that is used to learn _𝜃𝑖_ . We can tune this training reward _𝑟𝑖_<sup>train</sup> to capture different types of relations among the agents: 1) we can set _𝑟𝑖_<sup>train</sup> as the _individual reward 𝑟𝑖_ of each agent to model the competition among agents, and the resulting IL is called competitive IL ( **CM-IL** ); and 2) we can also set _𝑟𝑖_<sup>train</sup> as the _total reward 𝑟_<sup>tot</sup> =<sup>�</sup><sup>_𝑛_</sup> _𝑖_ =1<sup>_𝑟𝑖_of all</sup> agents, the social welfare of the multi-agent system, under which all the agents jointly optimize the performance of the whole system. We refer to the corresponding IL as cooperative IL ( **CO-IL** ). 

We also interpret the cooperative and competitive relations of agents in the context of ad auctions. Consider a one-round auction with two agents, the impression values of which are _𝑣_ 1 and _𝑣_ 2, respectively (assume _𝑣_ 1 _> 𝑣_ 2 without loss of generality). The relation is _cooperative_ if their bids satisfy _𝑏_ 1 _> 𝑏_ 2, otherwise is _competitive_ . This interpretation accords with the intuition that cooperation contributes to better social welfare. 

## **3 BEHAVIORS OF INDEPENDENT LEARNERS** 

In this section, we demonstrate the interaction results of CM-IL and CO-IL agents in the context of auto-bidding, through numerical experiments in a simplified two-agent bidding environment. We find that for CM-IL agents, the phenomena of oligarch emerges, leading to fierce competition and worse social welfare, while CO-IL 


![](assets/wsdm22/wsdm22.pdf-0004-00.png)



![](assets/wsdm22/wsdm22.pdf-0004-01.png)



![](assets/wsdm22/wsdm22.pdf-0004-02.png)


<!-- Start of picture text -->
(a) Agent 1’s winning values for CM-IL (b) Agent 1’s winning values for CO-IL<br>(c) Social welfare for CM-IL (d) Social welfare for CO-IL<br>(e) Revenue for CM-IL (f) Revenue for CO-IL<br><!-- End of picture text -->

**Figure 2: Converged performance of CM-IL and CO-IL.** 

agents achieve better social welfare, however, at the cost of reducing the platform’s revenue. 

We devise an auction environment with two bidding agents, which can be implemented with either the paradigm of competitive CM-IL or cooperative CO-IL. We vary the experimental settings with different total budget _𝐵_ 0 (normalized) in each episode and the budget ratio _𝑟_ , which controls the percentage of the total budget to agent 1. Thus the budgets for the two agents are _𝐵_ 1 = _𝐵_ 0 × _𝑟_ and _𝐵_ 2 = _𝐵_ 0 × (1 − _𝑟_ ), respectively. Both agents’ impression values are sampled from the normal distribution with mean 0 _._ 5 and variance 1. We train CM-IL and CO-IL for 50 _𝑘_ episodes, following the training principles discussed above. We examine their final performance in terms of three metrics: 1) agent 1’s total winning values, 2) social welfare of the auction and 3) revenue of the auction. Social welfare is the sum of two agents’ winning values, and revenue is the total payment calculated with Generalized Second Price (GSP) mechanism [6]. We omit the total winning values for agent 2, as it can be derived by subtracting agent 1’s winning value from the corresponding social welfare, e.g., we can derive that for _𝑟_ = 0 _._ 7, agent 2’s winning values are (19, 19, 16, 21) under different values of _𝐵_ 0. We plot the experimental results in Figure 2. Each number in the cell denotes agent 1’s obtained winning values, social welfare or revenue with specific experimental parameters (i.e., _𝐵_ 0 and _𝑟_ ). 

Figure 2(a) shows the total winning values of agent 1. Given an unbalanced budget setting _𝑟_ = 0 _._ 7, we observe that agent 1’s total winning values (39 _,_ 38 _,_ 41 _,_ 36) under different total budget _𝐵_ 0, are significantly larger than those of agent 2 (19 _,_ 19 _,_ 16 _,_ 21). 


![](assets/wsdm22/wsdm22.pdf-0004-07.png)


**Figure 3: The architecture of MAAB.** 

This indicates that agent 1 dominates most impressions by bidding aggressively, leading to a phenomenon of _oligarch_ [4]. The emergent oligarch worsens the social welfare. As shown in Figure 2(c) and Figure 2(d), CM-IL achieves the less social welfare than CO-IL, especially in enough budget settings, e.g., when _𝐵_ 0 = 1, CO-IL’s social welfare (64 _,_ 64 _,_ 64) are larger than those of CM-IL (57 _,_ 56 _,_ 58). 

A proper cooperation improves the social welfare by preventing the emergent oligarch. This can be seen by comparing Figure 2(a) with 2(b): agent 1’s total winning values decrease from (39 _,_ 38 _,_ 41 _,_ 36) to (35 _,_ 38 _,_ 33 _,_ 33) with more budget ( _𝑟_ = 0 _._ 7), and increase from (20 _,_ 16 _,_ 17 _,_ 22) to (20 _,_ 25 _,_ 28 _,_ 30) with less budget ( _𝑟_ = 0 _._ 3). This suggests that CO-IL assigns the impression opportunity mostly according to the value of impression instead of the budget, which turns out to be a better equilibrium in terms of social welfare in these settings. 

However, the above assign-by-value rule taken by CO-IL agents may sacrifice some advertisers’ profits to achieve better social welfare. Besides, Figure 2(e) and Figure 2(f) also show that cooperation also lowers the platform’s revenue. For example, when _𝐵_ 0 = 1, the revenues achieved by CO-IL agents (28, 26, 30) are significantly lower than those of CM-IL agents (69, 85, 71). This is because CO-IL agents have learned a collusion behavior of bidding low prices to reserve more budget. 

The opposite behaviors of the competitive approach and its cooperative counterpart come to two extremes: oligarch arises in the former approach under unbalanced budget settings, which causes worse social welfare. In contrast, the cooperative approach achieves better social welfare, however, at the cost of reducing the platform’s revenue and may potentially sacrifice some advertisers’ profits for achieving better social welfare. 

## **4 METHODS** 

In this section, we present our multi-agent framework MAAB, aiming to achieve good social welfare while guaranteeing the platform’s revenue. The architecture of MAAB is shown in Figure 3, and the training procedure is provided in Appendix A. 

## **4.1 Mixing Cooperation and Competition** 

Motivated by the extreme behaviors of CM-IL and CO-IL, we propose a reward assignment scheme, called temperature regularized credit assignment (TRCA), to establish a mixed cooperativecompetitive (MCC) [27] relation among agents. 

The main idea is to set a parameter _𝛼𝑖_ weighting each agent’s contribution to the total reward. The reward for each agent _𝑖_ can be written as 


![](assets/wsdm22/wsdm22.pdf-0005-01.png)


exp{ _𝑏𝑖_ <u>/</u> _𝜏_ <u>}</u> where _𝛼𝑖_ = <u>�</u> _<u>𝑛𝑗</u>_ =1<sup>exp{</sup><sup>_𝑏𝑗_/</sup><sup>_𝜏_}is a softmax-style weighting parameter</sup> that satisfies _𝛼𝑖_ ∈[0 _,_ 1] and<sup>�</sup><sup>_𝑛_</sup> _𝑖_ =1<sup>_𝛼𝑖_=1. The</sup><sup>_𝜏_is a temperature</sup> parameter balancing the extent of competition and cooperation. The intuition behind Eq. 4 is that the highest bid dominates the value of _𝑟_<sup>tot</sup> , while a lower bid has little influence on it. Thus, the assigned reward _𝑟𝑖_<sup>TRCA</sup> for each agent should increase with her bid, which is achieved by setting _𝛼𝑖_ in proportion to _𝑏𝑖_ by a softmax function. 

Our designed reward function also encodes both social welfare and revenue. The social welfare, measured by _𝑟_<sup>_𝑡𝑜𝑡_</sup> , appears in Eq. 4 directly, while the revenue contributed by each agent is implicitly expressed by her bid, as higher bids collected from all agents usually leads to higher revenue under the GSP auction. 

In addition, the temperature parameter _𝜏_ in Eq. 4 enables the co-existence of competition and cooperation, and works as a convenient tool to make a trade-off between these two relations. To illustrate this, we theoretically investigate how the value of _𝜏_ affects the bidding behaviors and the relations between agents in the simplified case of two agents. 

Theorem 4.1. _Consider a two-agent bidding case with impression values satisfying 𝑣_ 1 _> 𝑣_ 2 _in one round auction. Let 𝑏_ 1 _,𝑏_ 2 ∈ [ _𝑏𝑚𝑖𝑛,𝑏𝑚𝑎𝑥_ ] _denote two agents’ bids, where 𝑏𝑚𝑖𝑛 and 𝑏𝑚𝑎𝑥 are the minimum and maximum allowable bids respectively. If 𝑣_ 1 ≥ 2 _𝑣_ 2 _or_ 


![](assets/wsdm22/wsdm22.pdf-0005-06.png)


_then 𝑏_ 1 ≥ _𝑏_ 2 _, i.e., the relation between the two agents is cooperative, otherwise is competitive._ 

The proof could be found in Appendix B. The above theorem indicates that when _𝜏_ is larger than a threshold, agent 2 would prefer to cooperate; otherwise, she would behave competitively. Note that if the impression value _𝑣_ 1 is sufficiently large, i.e., _𝑣_ 1 ≥ 2 _𝑣_ 2, then agent 2 would always cooperate<sup>2</sup> , regardless of the value of _𝜏_ . We can safely conclude that a mixed cooperative-competitive relation among agents arises from setting _𝜏 >_ 0, and the relation tends to be more cooperative by setting a large _𝜏_ , while more competitive by setting a small _𝜏_ . The hyper-parameter _𝜏_ works as a proxy, through which the trade-off between competition and cooperation can be carefully controlled. 

## **4.2 Improving Revenue with Bar Agents** 

Although the cooperative approach contributes to a better social welfare, it leads to the aforementioned collusion behaviors which hurts the platform’s revenue. In this subsection, we introduce bar agents with different versions to avoid this. 

The simplest way to improve the revenue is to set a **fixed bidding bar** _𝑏_<sup>¯</sup> . If the auto-bidding agent’s bid satisfies _𝑏𝑖_ ≥ _𝑏_<sup>¯</sup> , the 

> 2In practice, even when _𝑣_ 1 ≥ 2 _𝑣_ 2, agent 2 may not cooperate when _𝜏_ → 0, which is slightly different from the derived result in theorem. This is because when _𝜏_ → 0, softmax function would consistently output _𝛼_ 1 = _𝛼_ 2 = 0 _._ 5 if _𝑏_ 1 = _𝑏_ 2, but _𝛼_ 1 = 1 and _𝛼_ 2 = 0 if _𝑏_ 1 _> 𝑏_ 2. However, in reality, their bids are hardly to be exactly the same, enabling our TRCA to establish a fully competitive case by setting _𝜏_ → 0. 

assigned reward for her is set to _𝑟𝑖_<sup>train</sup> = _𝑟𝑖_<sup>TRCA</sup> , otherwise _𝑟𝑖_<sup>train</sup> = 0. However, the fixed bidding bar needs to be tuned elaborately to obtain satisfactory performance. A large value may badly reduce the advertisers’ utilities, while an excessively small one may not effectively boost the revenue. 

A more advanced method is setting an **adaptive bidding bar** for each impression opportunity to optimize the revenue. One can introduce a bar agent implemented by reinforcement learning (RL) to achieve this, with bidding bar as bar agent’s action and available information of the impression opportunity as observation. However, the reward function for the bar agent is not trivial to define. Simply defining the payment of each auction as the reward for bar agent would lead to an extremely large bidding bar that may reduce social welfare. Besides, this method also ignores the fact that different auto-bidding agents usually have different budgets and values when competing for the same impression opportunity, implying that the same bidding bar may not be a good choice. 

Based on the above analysis, we propose personalized bidding bar agents to improve the revenue. In Figure 3, MAAB introduces **multiple bar agents** { ¯ _𝜋𝑖_ }<sup>_𝑛_</sup> _𝑖_ =1<sup>,witheachbaragent</sup><sup>_𝜋_¯</sup><sup>_𝑖_aimingat</sup> setting a personalized bar _𝑏_<sup>¯</sup> _𝑖_ for the corresponding auto-bidding agent _𝜋𝑖_ . Each bar agent shares the same observation as its corresponding auto-bidding agent. At each timestep, bar agents and the auto-bidding agents give their bidding bars { _𝑏_<sup>¯</sup> _𝑖_ }<sup>_𝑛_</sup> _𝑖_ =1<sup>and bids</sup> { _𝑏𝑖_ }<sup>_𝑛_</sup> _𝑖_ =1<sup>,respectively.Butonly{</sup><sup>_𝑏𝑖_}</sup><sup>_𝑛_</sup> _𝑖_ =1<sup>aresubmittedtotheauc-</sup> tion. Then the auction environment returns the payment _𝑝_ and the rewards { _𝑟𝑖_ }<sup>_𝑛_</sup> _𝑖_ =1<sup>. The rewards {</sup><sup>_𝑟𝑖_}</sup><sup>_𝑛_</sup> _𝑖_ =1<sup>are re-assigned by TRCA,</sup> obtaining { _𝑟𝑖_<sup>TRCA</sup> }<sup>_𝑛_</sup> _𝑖_ =1<sup>. However, using the payment</sup><sup>_𝑝_as the reward</sup> for bar agents may lead to extremely large bidding bars according to the previous discussion. To circumvent this, we propose a reward scheme called **bar gate** . The bar gate outputs a scalar _𝑧𝑖_ = _𝑧_ ( _𝑏_<sup>¯</sup> _𝑖,𝑏𝑖_ ) ∈{0 _,_ 1} for each pair of auto-bidding agent and bar agent, indicating whether each auto-bidding agent’s bid exceeds the bidding bar. The rule underlying the bar gate is given by 


![](assets/wsdm22/wsdm22.pdf-0005-16.png)


= With the bar gate, the rewards for optimizing _𝜋𝑖_ and _𝜋_ ¯ _𝑖_ are _𝑟𝑖_<sup>train</sup> _𝑧𝑖_ × _𝑟𝑖_<sup>TRCA</sup> and _𝑟_ ¯ _𝑖_<sup>train</sup> = _𝑧𝑖_ × _𝑝_ , respectively. It is worth to note that bar agents are introduced during the training phase but removed during the execution time. 

The bar agents and auto-bidding agents are trained simultaneously via an adversarial manner. The training procedure for _𝜋_ ¯ _𝑖_ is to optimize the bidding bar _𝑏_<sup>¯</sup> _𝑖_ , maximizing the revenue, while the auto-bidding agent _𝜋𝑖_ wants to lower her bid to reserve more budget due to the cooperation relation. The bar gate connects these two different goals by enforcing the bar agent’s bidding bar to be a maximum lower bound of auto-bidding agents’ bid. 

The proposed multiple bar agents and the reward scheme underlying the bar gate allow us to improve revenue by raising the auto-bidding agents’ bids to an appropriate level. It is worth to note that the bidding bar is similar to the reserve prices [22, 24], but differs in that the bidding bar requires no modification to the GSP mechanism [6] as it is only introduced during the training phase. 


![](assets/wsdm22/wsdm22.pdf-0006-00.png)


**Figure 4: Modeling with mean agent approach.** 

## **4.3 Modeling Large-Scale Multi-Agent System** 

In practical system, there may be millions of advertisers competing for billions of impressions every day, making it hard to train so many agents simultaneously by formulating each fine-grained advertiser as an agent, due to both the sparsity of the rewards and the limited resources (e.g., computational resources, time). We introduce our mean agent approach, which aims at providing a feasible and general method for the training of the large-scale multi-agent system for auto-bidding. 

One can take a high-level perspective such as _grouping_ [14]. By grouping advertisers by a certain principle, the rewards are no longer sparse at the group-level, and we only need to simultaneously train a separate policy for each high-level group instead of for each fine-grained advertiser. Our proposed mean agent first group advertisers by the _objective_ , as the main difference between advertisers lies in their optimizing objectives. Other principles may be possible depending on the specific situation. The grouping by objective results in a set of groups { _𝐺_ 1 _,𝐺_ 2 _,_ · · · _,𝐺𝑛_ }, where _𝐺𝑖_ is a set containing all the advertisers belonging to this group. However, it is not a trivial work to train such a policy _𝜋𝑖_ for group _𝐺𝑖_ that can be properly shared by all advertisers _𝑘_ ∈ _𝐺𝑖_ to generate their bids. This is due to the following two reasons: 1) the _𝑄_ -learning updating rule requires calculating the maximum action value for the next state, but the next state on the group-level is not clear; 2) advertisers usually have different budgets and values when competing for the same impression opportunity, making the policy sharing across different advertisers within the same group difficult. 

To handle the above issues, our mean agent approach considers the mean effects from a high-level perspective. The diagram of our mean agent approach is shown in Figure 4. The main idea is that, for each group, we train a mean policy _𝜋𝑖_ that calculates the mean bid based on the mean value and budget, and let each advertiser within the group derive her bid based on her value’s _advantage_ over the mean value. 

Before giving the full details of our modeling, we first introduce some notations. We consider a timestep as a period of time (e.g., 15 minutes), during which a number of impression opportunities arriving sequentially. We denote _𝑒_ ∈ _𝐸𝑡_ as an impression opportunity, where _𝐸𝑡_ is a set containing all opportunities within timestep _𝑡_ . The _𝑣𝑖,𝑘_<sup>_𝑒_is the value of advertiser</sup><sup>_𝑘_∈</sup><sup>_𝐺𝑖_for impression opportunity</sup><sup>_𝑒_.</sup> The _𝑥𝑘_<sup>_𝑒_∈{0</sup><sup>_,_1} indicates whether advertiser</sup><sup>_𝑘_wins the impression</sup> opportunity _𝑒_ . Advertiser _𝑘_ wins the impression if she has the maximum effective cost-per-mille (eCPM) ranking score _𝑝𝐶𝑇𝑅𝑘_<sup>_𝑒_×</sup><sup>_𝑏_</sup> _𝑘_<sup>_𝑒_.</sup> The specific modeling under the framework of Markov Games [17] is explained as follows. 

**Observation space** : the observation of mean agent _𝑖_ at timestep _𝑡_ is defined as _𝑜𝑖_<sup>_𝑡_=(</sup><sup>_𝐵_</sup> _𝑖_<sup>_𝑡, 𝑣_</sup> _𝑖_<sup>_𝑡,𝑡𝑠_</sup> _𝑖_<sup>_𝑡_).The</sup><sup>_𝐵_</sup> _𝑖_<sup>_𝑡_ismeanagent’sremain-</sup> ing budget at this timestep, and the initial budget of mean agent is set to _𝐵𝑖_<sup>1=</sup> | _𝐺_ <u>1</u> _𝑖_ | � _𝑘_ ∈ _𝐺𝑖_<sup>_𝐵_</sup> _𝑘_<sup>.Themeanvalue</sup><sup>_𝑣_</sup> _𝑖_<sup>_𝑡_=E[</sup><sup>_𝑣_</sup> _𝑖,𝑘_<sup>_𝑒_]≈</sup> | _𝐺𝑖_ |×|1 _𝐸𝑡_ | � _𝑒_ ∈ _𝐸𝑡 ,𝑘_ ∈ _𝐺𝑖_<sup>_𝑣_</sup> _𝑖,𝑘_<sup>_𝑒_. The</sup><sup>_𝑡𝑠_</sup> _𝑖_<sup>_𝑡_is timesteps left along the episode.</sup> **Action space** : each mean agent takes mean bid _𝑏𝑖_<sup>_𝑡_∈A</sup><sup>_𝑖_asits</sup> action. The bid of advertiser _𝑘_ ∈ _𝐺𝑖_ for impression opportunity _𝑒_ is _𝑏𝑖,𝑘_<sup>_𝑒_=</sup><sup>_𝑏_</sup> _𝑖_<sup>_𝑡_×</sup><sup>_𝑐𝑙𝑖𝑝_(</sup><sup>_𝐴_</sup> _𝑖,𝑘_<sup>_𝑒_),where</sup><sup>_𝐴_</sup> _𝑖,𝑘_<sup>_𝑒_=</sup><sup>_𝑣_</sup> _𝑖,𝑘_<sup>_𝑒_/</sup><sup>_𝑣𝑖_isdefinedasthe</sup> _advantage_ of _𝑣𝑖,𝑘_<sup>_𝑒_over the mean value. The advantages are clipped</sup> for preventing advertisers having excessively large values. **Reward function** : reward function is defined at the group-level [31] due to the large number of impressions and advertisers. Mean agent _𝑖_ ’s reward is defined as _𝑟𝑖_<sup>_𝑡_=</sup> | _𝐸_ <u>1</u> _𝑡_ | � _𝑒_ ∈ _𝐸𝑡 ,𝑘_ ∈ _𝐺𝑖_<sup>_𝑣_</sup> _𝑖,𝑘_<sup>_𝑒_×</sup><sup>_𝑥_</sup> _𝑘_<sup>_𝑒_.</sup> **Transition function** : The impression-level payment for winning impression _𝑒_ is _𝑝_<sup>_𝑒_</sup> = _𝑝𝐶𝑇𝑅_<sup>_𝑒_</sup> _𝑗_<sup>×</sup><sup>_𝑏𝑒_</sup> _𝑗_<sup>inexpectation,where</sup><sup>_𝑗_isthe</sup> index of the next ranked advertiser according to maximum eCPM ranking score. The payment for the mean agent is also defined at the group-level: _𝑝𝑖_<sup>_𝑡_= �</sup> _𝑒_ ∈ _𝐸𝑡 ,𝑘_ ∈ _𝐺𝑖_<sup>_𝑝𝑒_×</sup><sup>_𝑥_</sup> _𝑘_<sup>_𝑒_. Thus each mean agent’s</sup> next observation _𝑜𝑖_<sup>_𝑡_+1</sup> = ( _𝐵𝑖_<sup>_𝑡_−</sup><sup>_𝑝_</sup> _𝑖_<sup>_𝑡, 𝑣_</sup> _𝑖_<sup>_𝑡_+1</sup> _,𝑡𝑠𝑖_<sup>_𝑡_−1). Mean agent’s action</sup> is forced to 0 when its budget is below 0. 

Note that, for online deployment, the mean policy for a group is shared by all advertisers within the group to generate their bids separately without calculating advantages. The mean agent modeling can also be easily generalized to our proposed TRCA and bar agents approaches by replacing the bids and bidding bars with the corresponding mean ones. 

## **5 EXPERIMENTS** 

We evaluate our method in an offline industrial dataset and perform an online A/B test on the Alibaba e-commerce advertising platform. 

## **5.1 Offline Dataset Simulation** 

We perform the offline evaluation on a real offline dataset from Alibaba’s advertising system where on average 10 billion auctions are covered per day. See Appendix C for the environmental setup and implementation details. 

**Offline Dataset.** The offline dataset is extracted from the six-hour search auction log of November 18, 2020, including 705,140 impression opportunities. In each impression opportunity, nearly 400 ads are recalled to compete for displaying. Each recalled ad is associated with an advertiser’s id, timestamp, objective, impression value, manually set bid, etc. The objectives are mainly of three types – the number of clicks (pCTR), conversions (pCVR × pCTR), and add-tocarts (pCART × pCTR), which corresponds to three groups (CLICK, CONV, CART) in our experiments. A similar preprocessing as [14] is adopted: we randomly sample 1/150 of the logged impressions from the whole dataset for training, and the dataset for testing is sampled in the same way. 

**Evaluation Metrics.** We adopt the following evaluation metrics: 1) social welfare, which is calculated by adding up the normalized total values won by three groups ; 2) platform’s revenue, which is defined as the cumulative payments along the episode. The payment at each timestep is calculated by GSP-based expected Cost-Per-Click (CPC). The evaluation procedure is provided in Appendix C.1. 

**Table 1: Mean and standard deviation of different groups’ values (CLICK, CONV, CART), platform’s revenue, and social welfare in offline dataset simulation.** 

|Setting 1|CLICK|CONV|CART|Revenue|Social Welfare|
|---|---|---|---|---|---|
|MSB|24.7±0|21.8±0|18.0±0|16.9±0|64.5±0|
|DQN-S|**29.3**±2.7|35.8±5.1|**36.0**±2.3|68.3±6.7|101.0±2.5|
|CM-IL|27.8±0.9|41.3±0.7|35.0±0.8|**86.8**±1.2|104.1±0.8|
|CO-IL|27.3±1.5|41.3±2.0|**35.6**±1.7|66.9±10.2|104.3±2.3|
|MAAB|28.0±0.8|**41.8**±1.3|35.5±1.4|80.6±3.2|**105.3**±1.3|
|Setting 2|CLICK|CONV|CART|Revenue|Social Welfare|
|MSB|24.7±0|21.8±0|18.0±0|16.9±0|64.5±0|
|DQN-S|**37.1**±2.1|25.1±3.1|34.8±1.8|75.5±5.2|97.0±2.3|
|CM-IL|35.3±1.3|29.2±1.0|35.1±0.8|**85.0**±2.9|99.6±0.6|
|CO-IL|30.7±3.3|**35.3**±3.2|37.0±2.7|52.9±12.4|103.0±2.4|
|MAAB|31.3±1.2|33.5±1.7|**38.6**±1.4|69.0±3.6|**103.4**±0.7|



**Budget Constraints.** For the offline experiments, we first calculate the total payment of an episode by enforcing all mean agents using their maximum mean bids, and accumulate the total payment _𝑃_ =<sup>�</sup> _𝑡_ � _𝑒_ ∈ _𝐸𝑡_<sup>_𝑝𝑒_. Then the budget of advertiser</sup><sup>_𝑘_∈</sup><sup>_𝐺_</sup> _𝑖_<sup>and</sup> mean agent _𝑖_ are set as a fraction of the episode’s total payment: _𝐵𝑖_ = _𝐵𝑘_ = _𝑃_ × _𝐵_ 0 × _𝑟_ [ _𝑖_ ]. We run the evaluation with _𝐵_ 0 = 1/4 and _𝑟_ = [1 _,_ 1 _,_ 1] _,_ [1 _._ 5 _,_ 0 _._ 5 _,_ 1]. 

**Compared Methods.** With the same settings, the following methods are selected for comparisons: 1) **MSB** uses advertisers’ manually set bids for bidding. 2) **DQN-S** can be seen as the single-agent version of IL. Specifically, we train a mean policy for each group using DQN [21] by assuming other advertisers use their manually set bids. However, all mean agents use their trained policies for auction during testing rather than considering other advertisers’ bids as the manually set ones. 3) **CM-IL** [28]. 4) **CO-IL** . 5) **MAAB** is our proposed method, which is the mixed cooperation-competitive IL augmented with bar agents. 

**Experimental Results.** We test the performance under the following two settings: 1) _𝐵_ 0 = 1/4 and _𝑟_ = [1 _,_ 1 _,_ 1], in which case all auto-bidding agents have equal budget constraints; 2) _𝐵_ 0 = 1/4 and _𝑟_ = [1 _._ 5 _,_ 1 _,_ 0 _._ 5], which is an unbalanced budget setting. The main results are shown in Table 1. The reported performance is averaged over 3 independent runs after training for 3.5 million timesteps. 

We find that traditional way of manually setting bids (MSB) fails to achieve good performance – social welfare is 64.5 and platform’s revenue is 16.9, which is consistently the worst among all methods. By comparison, DQN-S is superior in terms of the three groups’ values (29.3, 35.8, 36.0), social welfare (101.0) and platform’s revenue (68.3), due to the budget spending controlled by RL. 

However, the performance of DQN-S is still limited by the unreliable assumption that other agents’ bids are fixed. This assumption can be further removed by adopting a multi-agent learning paradigm. The benefits of multi-agent learning can be demonstrated by CM-IL’s superior performance over DQN-S both in terms of social welfare (e.g., 104.1 > 101.0 in setting 1) and platform’s revenue (e.g., 86.8 > 68.3 in setting 1). CM-IL learns auto-bidding policies simultaneously, making it possible to model the interactions between agents explicitly. However, the competitive relation may not help 

**Table 2: Mean of different groups’ values (CLICK, CONV, CART), platform’s revenue and social welfare in the online production environment.** 

||CLICK|CONV|CART|Revenue|Social Welfare|
|---|---|---|---|---|---|
|CM-IL|31.4|48.2|20.4|**100.0**|100.0|
|MAAB|**32.9**|**50.3**|**21.4**|96.1|**104.6**|



achieve better social welfare, which can be seen by comparing CMIL with CO-IL. CO-IL models the relations between auto-bidding agents in a cooperative way and is slightly better than CM-IL in social welfare (104.3 > 104.1 in setting 1 and 103.0 > 99.6 in setting 2), however, at the cost of reducing the platform’s revenue (66.9 < 86.8 in setting 1 and 52.9 < 85.0 in setting 2). 

In between these two extremes, MAAB uses TRCA and models the relation between agents in the MCC way, which achieves a better equilibrium between social welfare and the revenue. As shown in Table 1, MAAB achieves better social welfare compared with CM-IL (105.3 > 104.1 in setting 1 and 103.4 > 99.6 in setting 2) and significantly outperforms CO-IL in terms of the revenue (80.6 > 66.9 in setting 1 and 69.0 > 52.9 in setting 2). 

## **5.2 Online Experiments** 

To further verify our MAAB method’s validity, we have launched it to the online real production environment (Taobao display advertising system) and compared it with the baseline method CM-IL. The deployment has the following details: 1) _𝑄_ networks in both methods are trained on a Tensorflow-based distributed training framework and updated every 2 hours. 2) More features (such as pCTR, pCVR, etc.) are encoded into the observation in both methods for better modeling the dynamic environment. 3) As mentioned in subsection 4.3, during online deployment, the bid for each ad is generated by feeding each ad’s encoded observation into the corresponding mean policy. 

The main results of the online A/B test with 1% of whole production traffic from January 30, 2021 to February 3, 2021 are shown in Table 2. Since real online data needs to be kept confidential, we normalized the baseline method’s performance to 100. Similar to the results of offline experiments, compared with CM-IL, MAAB achieves better social welfare, but with a lower revenue (96.1 < 100). 

## **5.3 Ablation Study** 

This section investigates the effectiveness of TRCA and the necessity of bar agents for improving platform’s revenue. 

_5.3.1 Effectiveness of TRCA._ To investigate the effectiveness of the proposed TRCA for modeling the cooperative and competitive relation, we remove the bar agents in MAAB and call the resulting method MIX-IL. Then we adjust the parameter _𝜏_ in MIX-IL and perform experiments with our offline dataset, where a larger _𝜏_ corresponds to more cooperative whereas a smaller _𝜏_ corresponds to more competitive. Especially, _𝜏_ = 0 is equivalent to CM-IL; _𝜏_ = ∞ is equivalent to CO-IL. We set _𝐵_ 0 = 1/4 and _𝑟_ = [1 _._ 5 _,_ 0 _._ 5 _,_ 1]. 

As shown in Figure 5(a), after training for 2 million timesteps, COIL and MIX-IL achieve nearly the same social welfare (101.2, 103.1 


![](assets/wsdm22/wsdm22.pdf-0008-00.png)



![](assets/wsdm22/wsdm22.pdf-0008-01.png)



![](assets/wsdm22/wsdm22.pdf-0008-02.png)


<!-- Start of picture text -->
(a) Social welfare (b) Platform’s revenue<br><!-- End of picture text -->

**Figure 5: Social welfare and platform’s revenue for methods with different parameter** _𝜏_ **. The mean and 95% confidence interval are shown across 3 independent runs.** 

and 101.9 for _𝜏_ = 2 _,_ 4 and ∞ respectively), and they consistently outperform CM-IL (99.6), which suggests cooperation can help achieve better social welfare. However, Figure 5(b) illustrates the side effect of cooperation. A fully cooperative approach would significantly reduce the platform’s revenue (57.5), while a competitive approach guarantees a higher platform’s revenue (79.3) due to the competition. In between these two extremes, MIX-IL ( _𝜏_ = 2) seemingly achieves a better equilibrium that guarantees good social welfare (101.2) comparable with the fully cooperative one (101.8) and improves platform’s revenue (74.8 > 57.5). In summary, to achieve a win-win situation for advertisers and the platform, it seems necessary to balance the competition and cooperation in multi-agent auto-bidding problem, and _𝜏_ could serve as a convenient tool to achieve such a balance. 

_5.3.2 Influence of Bar Agents._ We investigate necessity of bar agents for improving platform’s revenue and the effectiveness of adaptive bidding bars. To this end, we compare MAAB against the following two methods in offline dataset simulation: 1) MIX-IL: this method is derived from MAAB by removing bar agents; 2) MAAB-fix: we fix bar agents’ actions to be a heuristic value ( _𝑏_<sup>¯</sup> = 1 and _𝑏_<sup>¯</sup> = 4) in MAAB, which can be seen as the _fixed bidding bar_ introduced in subsection 4.2. All methods are trained for 2 million timesteps, and we set _𝐵_ 0 = 1/2 and _𝑟_ = [1 _._ 5 _,_ 0 _._ 5 _,_ 1]. Here we use a larger _𝐵_ 0, which corresponds to more budget in total and can help better illustrate the bar agents’ effectiveness in improving the platform’s revenue. 

As shown in Table 3, by comparing MIX-IL with MAAB-fix ( _𝑏_<sup>¯</sup> = 1 or _𝑏_<sup>¯</sup> = 4), we can see that the idea of setting a bidding bar could improve the platform’s revenue. For example, platform’s revenue increases from 99.6 to 114.3 by using bidding bar _𝑏_<sup>¯</sup> = 1 in MIX-IL, and further increases to 164.9 by raising the bidding bar to _𝑏_<sup>¯</sup> = 4. However, a large bidding bar (i.e., _𝑏_<sup>¯</sup> = 4) would hurt the social welfare, while a small bidding bar (i.e., _𝑏_<sup>¯</sup> = 1) still leaves room for further improvement of platform’s revenue. The benefit of the adaptive bidding bar can be seen by comparing MAAB with MAAB-fix ( _𝑏_<sup>¯</sup> = 1). MAAB achieves comparable social welfare (103.9 ≈ 104 _._ 5) with MAAB-fix ( _𝑏_<sup>¯</sup> =1) and further improves platform’s revenue (134.6 > 114.3). Our adaptive bidding bar and the bar gate enable MAAB to improve the revenue without reducing the social welfare, which presents a clear benefit over the fixed one. See Appendix C.4 for additional analysis of the bar agents. 

**Table 3: Mean and standard deviation of social welfare and platform’s revenue.** 

||Social Welfare|Platform’s Revenue|
|---|---|---|
|MIX-IL|104.0±3.3|99.6±18.2|
|MAAB-fix (<sup>¯</sup>_𝑏_=1)|**104.5**±1.4|114.3±17.1|
|MAAB-fix (<sup>¯</sup>_𝑏_=4)|99.3±0.4|**164.9**±1.3|
|MAAB|103.9±1.2|134.6±8.2|



## **6 RELATED WORK** 

**Multi-Agent Reinforcement Learning.** Recent works have explored RL beyond single-agent scenarios and have considered multiagent case [19, 25, 28, 30]. In MARL literature, some works focus on learning cooperation [25, 26, 28], in which a team of agents takes actions to achieve a common goal. One of the challenges in learning cooperation is the credit assignment problem [9, 25, 26], i.e., the agents should deduce their contributions to the global rewards [13]. Our TRCA instead considers the credit assignment for establishing a MCC relation among agents, which differs from previous works in terms of both motivation and the problem settings. 

**Bid Optimization.** Bidding optimization is one of the key problems in real-time bidding. Several lines of work consult RL to learn the bidding strategies under constraints [2, 14, 31]. However, these works adopt a single-agent setting – they optimize the bid strategy under the assumption that the market price is stationary. A few studies also consider bid optimization from the multi-agent perspective. Jin et al. [14] formulate bid optimization with cooperative MARL and use a clustering method for dealing with the huge number of advertisers. However, the cooperative game may result in collusion behaviors that reduce the platform’s revenue. Concurrently to our work, Guan et al. [11] try to avoid the collusion behaviors by introducing an extra revenue constraint. We instead avoid collusion by modeling the MCC relation [27] among agents and design bar agents to improve the revenue further in an adversarial manner. To optimize revenue, most works focus on the reserve prices [22, 29] and designing revenue-maximizing auctions [5, 18], which is a different setting from ours as we consider the joint optimization of the advertiser’s bidding strategies and platform’s revenue without changing the GSP mechanism. 

## **7 CONCLUSIONS** 

In this work, we proposed a MARL framework, called MAAB, for the auto-bidding in online advertising through three contributions: 1) proposing TRCA for establishing a mixed cooperation and competition relation among agents, 2) using bar agents and a reward scheme, called bar gate, for improving the platform’s revenue with an adversarial training manner, 3) proposing a mean agent approach for the deployment of our methods on the large-scale advertising platform. Extensive offline and online experiments demonstrate the effectiveness of MAAB in achieving social welfare and guaranteeing the platform’s revenue. Our future work includes extending TRCA by dynamically tuning the temperature parameter based on real-time information. Besides, further investigation on the reward scheme underlying the bar gate is needed for the fast convergence of bar agents. 

## **REFERENCES** 

- [1] Gagan Aggarwal, Ashwinkumar Badanidiyuru, and Aranyak Mehta. 2019. Autobidding with constraints. In _WINE_ . Springer, 17–30. 

- [2] Han Cai, Kan Ren, Weinan Zhang, Kleanthis Malialis, Jun Wang, Yong Yu, and Defeng Guo. 2017. Real-time bidding by reinforcement learning in display advertising. In _WSDM_ . 661–670. 

- [3] Google Ads Help Center. 2021. About automated bidding. https://support.google. com/google-ads/answer/2979071. Accessed: January 24, 2021. 

- [4] Carl Davidson and Raymond Deneckere. 1986. Long-run competition in capacity, short-run competition in price, and the Cournot model. _The Rand Journal of Economics_ (1986), 404–415. 

- [5] Paul Dütting, Zhe Feng, Harikrishna Narasimhan, David Parkes, and Sai Srivatsa Ravindranath. 2019. Optimal auctions through deep learning. In _ICML_ . PMLR, 1706–1715. 

- [6] Benjamin Edelman, Michael Ostrovsky, and Michael Schwarz. 2007. Internet advertising and the generalized second-price auction: Selling billions of dollars worth of keywords. _American economic review_ 97, 1 (2007), 242–259. 

- [7] eMarketer. 2015. Worldwide retail ecommerce sales: eMarketer’s updated estimates and forecast through 2019. (2015). 

- [8] Facebook. 2021. Facebook. https://www.facebook.com/business/m/one-sheeters/ facebook-bid-strategy-guide. Accessed: January 24, 2021. 

- [9] Jakob Foerster, Gregory Farquhar, Triantafyllos Afouras, Nantas Nardelli, and Shimon Whiteson. 2018. Counterfactual multi-agent policy gradients. In _AAAI_ , Vol. 32. 

- [10] Google. 2021. Google AdWords API. https://developers.google.com/adwords/ api/docs/guides/start. Accessed: January 24, 2021. 

- [11] Ziyu Guan, Hongchang Wu, Qingyu Cao, Hao Liu, Wei Zhao, Sheng Li, Cai Xu, Guang Qiu, Jian Xu, and Bo Zheng. 2021. Multi-Agent Cooperative Bidding Games for Multi-Objective Optimization in e-Commercial Sponsored Search. _arXiv preprint arXiv:2106.04075_ (2021). 

- [12] Garrett Hardin. 2009. The tragedy of the commons. _Journal of Natural Resources Policy Research_ 1, 3 (2009), 243–253. 

- [13] Pablo Hernandez-Leal, Bilal Kartal, and Matthew E Taylor. 2019. A survey and critique of multiagent deep reinforcement learning. 33, 6 (2019), 750–797. 

- [14] Junqi Jin, Chengru Song, Han Li, Kun Gai, Jun Wang, and Weinan Zhang. 2018. Real-time bidding with multi-agent reinforcement learning in display advertising. In _CIKM_ . 2193–2201. 

- [15] Jean-Michel Lasry and Pierre-Louis Lions. 2007. Mean field games. _Japanese journal of mathematics_ 2, 1 (2007), 229–260. 

- [16] Joel Z Leibo and Marc Lanctot. 2017. Multi-agent Reinforcement Learning in Sequential Social Dilemmas. (2017). arXiv:arXiv:1702.03037v1 

- [17] Michael L Littman. 1994. Markov games as a framework for multi-agent reinforcement learning. In _Machine learning proceedings 1994_ . Elsevier, 157–163. 

- [18] Xiangyu Liu, Chuan Yu, Zhilin Zhang, Zhenzhe Zheng, Yu Rong, Hongtao Lv, Da Huo, Yiqing Wang, Dagui Chen, Jian Xu, Fan Wu, Guihai Chen, and Xiaoqiang 

Zhu. 2021. Neural Auction: End-to-End Learning of Auction Mechanisms for E-Commerce Advertising. In _SIGKDD_ . 3354–3364. 

- [19] Ryan Lowe, Yi I Wu, Aviv Tamar, Jean Harb, OpenAI Pieter Abbeel, and Igor Mordatch. 2017. Multi-agent actor-critic for mixed cooperative-competitive environments. In _NIPS_ . 6379–6390. 

- [20] Robert C Marshall and Leslie M Marx. 2007. Bidder collusion. _Journal of Economic Theory_ 133, 1 (2007), 374–402. 

- [21] Volodymyr Mnih, Koray Kavukcuoglu, David Silver, Andrei A Rusu, Joel Veness, Marc G Bellemare, Alex Graves, Martin Riedmiller, Andreas K Fidjeland, Georg Ostrovski, et al. 2015. Human-level control through deep reinforcement learning. _nature_ 518, 7540 (2015), 529–533. 

- [22] Mehryar Mohri and Andres Munoz Medina. 2014. Learning theory and algorithms for revenue optimization in second price auctions with reserve. In _ICML_ . PMLR, 262–270. 

- [23] Roger B Myerson. 1981. Optimal auction design. _Mathematics of operations research_ 6, 1 (1981), 58–73. 

- [24] Michael Ostrovsky and Michael Schwarz. 2011. Reserve prices in internet advertising auctions: A field experiment. In _EC_ . 59–60. 

- [25] Tabish Rashid, Mikayel Samvelyan, Christian Schroeder, Gregory Farquhar, Jakob Foerster, and Shimon Whiteson. 2018. QMIX: Monotonic Value Function Factorisation for Deep Multi-Agent Reinforcement Learning. In _ICML_ . 4295–4304. 

- [26] Peter Sunehag, Guy Lever, Audrunas Gruslys, Wojciech Marian Czarnecki, Vinícius Flores Zambaldi, Max Jaderberg, Marc Lanctot, Nicolas Sonnerat, Joel Z Leibo, Karl Tuyls, et al. 2018. Value-Decomposition Networks For Cooperative Multi-Agent Learning Based On Team Reward.. In _AAMAS_ . 2085–2087. 

- [27] Ardi Tampuu, Tambet Matiisen, Dorian Kodelja, Ilya Kuzovkin, Kristjan Korjus, Juhan Aru, Jaan Aru, and Raul Vicente. 2017. Multiagent cooperation and competition with deep reinforcement learning. _PloS one_ 12, 4 (2017), e0172395. 

- [28] Ming Tan. 1993. Multi-agent reinforcement learning: Independent vs. cooperative agents. In _ICML_ . 330–337. 

- [29] David RM Thompson and Kevin Leyton-Brown. 2013. Revenue optimization in the generalized second-price auction. In _EC_ . 837–852. 

- [30] Chao Wen, Xinghu Yao, Yuhui Wang, and Xiaoyang Tan. 2020. SMIX ( _𝜆_ ): Enhancing Centralized Value Functions for Cooperative Multi-Agent Reinforcement Learning.. In _AAAI_ . 7301–7308. 

- [31] Di Wu, Xiujun Chen, Xun Yang, Hao Wang, Qing Tan, Xiaoxun Zhang, Jian Xu, and Kun Gai. 2018. Budget constrained bidding by model-free reinforcement learning in display advertising. In _CIKM_ . 1443–1451. 

- [32] Xiao Yang, Daren Sun, Ruiwei Zhu, Tao Deng, Zhi Guo, Zongyao Ding, Shouke Qin, and Yanfeng Zhu. 2019. Aiads: Automated and intelligent advertising system for sponsored search. In _SIGKDD_ . 1881–1890. 

- [33] Yaodong Yang, Rui Luo, Minne Li, Ming Zhou, Weinan Zhang, and Jun Wang. 2018. Mean field multi-agent reinforcement learning. In _ICML_ . PMLR, 5571–5580. 

- [34] Shuai Yuan, Jun Wang, Bowei Chen, Peter Mason, and Sam Seljan. 2014. An empirical study of reserve price optimisation in real-time bidding. In _SIGKDD_ . 1897–1906. 

## **A ALGORITHM** 

### **Algorithm 1:** Training Procedure for MAAB 

Set the empty replay buffer D to capacity _𝑁_ D , _𝑠𝑡𝑒𝑝_ = 0, training batch size _𝑏_ ; Initialize Q-networks _𝑄𝑖_ and _𝑄_<sup>¯</sup> _𝑖_ with random parameters _𝜃𝑖_ and _𝜃_<sup>ˆ</sup> _𝑖_ , and the corresponding target networks with parameters _𝜃_<sup>ˆ</sup> _𝑖_ ← _𝜃𝑖_ and _𝜃_<sup>ˆ¯</sup> _𝑖_ ← _𝜃_<sup>¯</sup> _𝑖_ , for _𝑖_ = 1 _,_ · · · _,𝑛_ ; **while** _𝑠𝑡𝑒𝑝 < 𝑚𝑎𝑥_𝑠𝑡𝑒𝑝_ **do for** _𝑡_ = 1 _to 𝑇_ **do for** _each agent i_ **do** Obtain the observation _𝑜𝑖_ for agent _𝑖_ and bar agent _𝑖_ ; Select _𝑏𝑖_ according to _𝜖_ -greedy policy w.r.t _𝑄𝑖_ ; Select _𝑏_<sup>¯</sup> _𝑖_ according to _𝜖_ -greedy policy w.r.t _𝑄_<sup>¯</sup> _𝑖_ ; **end** Submit { _𝑏_ 1 _,_ · · · _,𝑏𝑛_ } to the auction environment; Get rewards { _𝑟_ 1 _,_ · · · _,𝑟𝑛_ } and the payment _𝑝_ ; Calculate _𝑟𝑖_<sup>TRCA</sup> according to Eq. 4; Get _𝑧𝑖_ = _𝑧_ ( _𝑏𝑖, 𝑏_<sup>¯</sup> _𝑖_ ) according to Eq. 6; Calculate _𝑟𝑖_<sup>train</sup> = _𝑧𝑖_ × _𝑟𝑖_<sup>TRCA</sup> and _𝑟_ ¯ _𝑖_<sup>train</sup> = _𝑧𝑖_ × _𝑝_ ; _𝑠𝑡𝑒𝑝_ = _𝑠𝑡𝑒𝑝_ + 1 **end** Store the episode in D, replacing the oldest episode if | _𝐷_ | _> 𝑁_ D ; Sample a batch of b episodes ∼ Uniform(D); **for** _each agent i_ **do** Set _𝑦𝑖_ = _𝑟𝑖_<sup>train</sup> + _𝛾_ max _𝑏𝑖_ ′<sup>_𝑄𝑖_(</sup><sup>_𝑜_</sup> _𝑖_<sup>′</sup><sup>_,𝑏_</sup> _𝑖_<sup>′;</sup><sup>_𝜃_ˆ);</sup> Set _𝑦_ ¯ _𝑖_ = _𝑟_ ¯ _𝑖_<sup>train</sup> + _𝛾_ max _𝑏_ ¯ _𝑖_ ′ _𝑄_ ¯ _𝑖_ ( _𝑜𝑖_<sup>′</sup><sup>_,𝑏_¯</sup> _𝑖_<sup>′;</sup><sup>_𝜃_ˆ¯);</sup> Update _𝜃𝑖_ by minimizing<sup>�</sup> _𝑏,𝑡_ �( _𝑦𝑖_ − _𝑄𝑖_ ( _𝑜𝑖,𝑏𝑖_ ; _𝜃𝑖_ ))<sup>2�</sup> ; Update _𝜃_<sup>¯</sup> _𝑖_ by minimizing<sup>�</sup> _𝑏,𝑡_ �� _𝑦_ ¯ _𝑖_ − _𝑄_ ¯ _𝑖_ � _𝑜𝑖, 𝑏_ ¯ _𝑖_ ; _𝜃_ ¯ _𝑖_ �� 2<sup>�</sup> twice; Replace target parameters _𝜃_<sup>ˆ</sup> _𝑖_ ← _𝜃𝑖_ every C episodes; Replace target parameters _𝜃_<sup>ˆ¯</sup> _𝑖_ ← _𝜃_<sup>¯</sup> _𝑖_ every C episodes; **end end** 

## **B PROOF OF THEOREM 4.1** 

Theorem 4.1. _Consider a two-agent bidding case with impression values satisfying 𝑣_ 1 _> 𝑣_ 2 _in one round auction. Let 𝑏_ 1 _,𝑏_ 2 ∈ [ _𝑏𝑚𝑖𝑛,𝑏𝑚𝑎𝑥_ ] _denote two agents’ bids, where 𝑏𝑚𝑖𝑛 and 𝑏𝑚𝑎𝑥 are the minimum and maximum allowable bids respectively. If 𝑣_ 1 ≥ 2 _𝑣_ 2 _or_ 


![](assets/wsdm22/wsdm22.pdf-0010-05.png)


_then 𝑏_ 1 ≥ _𝑏_ 2 _, i.e., the relation between the two agents is cooperative, otherwise is competitive._ 


![](assets/wsdm22/wsdm22.pdf-0010-07.png)


exp{ _𝑏_ <u>2/</u> _𝜏_ <u>}</u> where _𝛼_ 2 (b) = <u>�2</u> _𝑗_ =1<sup>exp{</sup><sup>_𝑏𝑗_/</sup><sup>_𝜏_}and</sup><sup>_𝐼_(·) is the indicator function. We</sup> define the the solution set of case L and H: _𝐿_ = {( _𝑏_ 1 _,𝑏_ 2)| _𝑏𝑚𝑎𝑥_ ≥ _𝑏_ 1 ≥ _𝑏_ 2 ≥ _𝑏𝑚𝑖𝑛_ }, _𝐻_ = {( _𝑏_ 1 _,𝑏_ 2)| _𝑏𝑚𝑎𝑥_ ≥ _𝑏_ 2 _> 𝑏_ 1 ≥ _𝑏𝑚𝑖𝑛_ }. Our goal 

is to find the condition that the optimal solution of Eq. 7 always lies in the case L, which can be transformed into the following target: 


![](assets/wsdm22/wsdm22.pdf-0010-10.png)


## **C OFFLINE DATASET SIMULATION** 

## **C.1 Environmental Setup** 

We adopt the modeling in subsection 4.3. We consider each hour as an episode of length 60, with each minute in an hour as a timestep. In implementation, the individual reward for each mean agent is normalized for the sake of calculating social welfare: for mean agent _𝑖_ at timestep _𝑡_ , we normalized the individual reward _𝑟𝑖_<sup>_𝑡_by dividing</sup> it by the maximum total value ( _𝑉𝑖_<sup>max</sup> =<sup>�</sup> _𝑡,𝑒_ ∈ _𝐸𝑡 ,𝑘_ ∈ _𝐺𝑖_<sup>_𝑣_</sup> _𝑖,𝑘_<sup>_𝑒_) that mean</sup> agent _𝑖_ could achieve along the episode. 

## **C.2 Evaluation Procedure** 

The evaluation procedure is similar to the training process. We evaluate the performance by pausing training after every 10,000 timesteps and running 5 independent test episodes with bar agents removed and each agent performing greedy action selection in a decentralized way. The reported performance is also normalized for better comparisons: for calculating the performance of each group, we first calculate the total value obtained by each group ( _𝑉𝑖_ = � _𝑡,𝑒_ ∈ _𝐸𝑡 ,𝑘_ ∈ _𝐺𝑖_<sup>_𝑣_</sup> _𝑖,𝑘_<sup>_𝑒_×</sup><sup>_𝑥_</sup> _𝑘_<sup>_𝑒_) and divide it by the maximum total value</sup> _𝑉𝑖_<sup>max</sup> that this group could achieve along the episode. _𝑉𝑖_ / _𝑉𝑖_<sup>max</sup> is adopted as the performance of the group. Social welfare is therefore calculated as the sum of group performance. 

## **C.3 Implementation Details** 

Each agent’s _𝑄_ or _𝑄_<sup>¯</sup> network is a fully connected neural network with 3 hidden layers and 64 nodes for each layer. Each _𝑄_ or _𝑄_<sup>¯</sup> network takes as input the observation that includes the remaining budget, mean value and the timesteps left along the episode, and outputs the state-action _𝑄_ or _𝑄_<sup>¯</sup> value for each candidate action. Each agent selects actions from the interval [0 _,_ 5] that is discretized into 21 equally spaced values, according to its _𝑄_ or _𝑄_<sup>¯</sup> network. 

During training, each agent explores the environment by following an _𝜖_ -greedy policy with linear _𝜖_ -annealing over 50k steps from 1.0 to 0.05. We uniformly sample 32 episodes from the replay buffer that contains the most recent 5000 episodes and perform a single training step on _𝑄_ networks after every episode. However, 


![](assets/wsdm22/wsdm22.pdf-0011-00.png)



![](assets/wsdm22/wsdm22.pdf-0011-01.png)



![](assets/wsdm22/wsdm22.pdf-0011-02.png)


<!-- Start of picture text -->
(a) Agents’ bids for MAAB (b) Payments for three methods<br><!-- End of picture text -->

**Figure 6: Agents’ bids for MAAB and the payments for three methods across each timestep of a selected episode. The curves are smoothed over a sliding window of size 3.** 

for faster convergence, _𝑄_<sup>¯</sup> networks are updated twice after every episode. The target networks for both _𝑄_ and _𝑄_<sup>¯</sup> are updated every 200 training episodes. 

To speed up the learning, mean agents and bar agents share the parameters of the _𝑄_ and _𝑄_<sup>¯</sup> network, respectively. Thus a onehot encoding of the agent id is concatenated onto each agent’s observations. All neural networks are trained using RMSprop with a learning rate 0 _._ 0005. We set _𝛾_ = 0 _._ 99 and _𝜏_ = 4. The advantages are clipped to the range [0, 3]. 

## **C.4 Additional Analysis of the Bar Agents** 

To further illustrate the effectiveness of bar agents for improving the platform’s revenue, we select an episode and plot the bids of 

two agents across each timestep. The episode is selected in the two-agent bidding environment for the simplicity of illustration. We set _𝐵_ 0 = 1 and _𝑟_ = 0 _._ 5. 

As shown in Figure 6(a), by comparing the solid line with the dotted line in the same color, we find that bar agents’ bids are strictly lower than those of their counterparts. This demonstrates the effectiveness of bar gate as the violation of rule _𝑏𝑖_ ≥ _𝑏_<sup>¯</sup> _𝑖_ in the bar gate prohibits both agents from receiving their rewards. Interestingly, our results also reveal that bar agents’ bids have a similar pattern as their counterparts. For example, both agent 1 (blue line) and bar agent 1 (blue dotted line) have a bidding peak at timestep 19 and a bidding valley at timestep 60. For agent 2 (red line) and its counterpart (red dotted line), similar patterns can also be found at timestep 40 and 62. These patterns demonstrate that bar agents, along with the bar gate, can adaptively set the bidding bar by utilizing additional information such as impression value and budget, which presents a clear benefit over MAAB-fix that does not utilize extra information when determining the bidding bar. 

In Figure 6(b), we also plot the payments for MAAB, MAAB-fix ( _𝑏_<sup>¯</sup> = 1) and MIX-IL across each timestep. We find that approaches with bidding bar (MAAB, MAAB-fix) outperform the one without it (MIX-IL) in terms of the payments, which implies that the bidding bar could improve the revenue. Besides, payments of MAAB are higher than MAAB-fix, which suggests adaptively setting the bidding bar is superior to a static one. 

