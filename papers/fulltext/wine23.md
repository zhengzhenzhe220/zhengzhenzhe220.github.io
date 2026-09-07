---
source: wine23.pdf
pages: 24
converter: pymupdf4llm
converted_at: 2026-08-30T22:11:41+08:00
---

# Auction Design for Bidders with Ex Post ROI Constraints 

Hongtao Lv<sup>1,3</sup> , Xiaohui Bei<sup>2</sup> , Zhenzhe Zheng<sup>3⋆</sup> , and Fan Wu<sup>3</sup> 

> 1 School of Software & Joint SDU-NTU Centre for Artificial Intelligence Research 

   - (C-FAIR), Shandong University, Jinan, China 

      - lht@sdu.edu.cn 

- 2 School of Physical and Mathematical Sciences, Nanyang Technological University, Singapore, Singapore 

xhbei@ntu.edu.sg 

> 3 Department of Computer Science and Engineering, Shanghai Jiao Tong University, Shanghai, China 

{zhengzhenzhe, wu-fan}@sjtu.edu.cn 

Abstract. Motivated by practical constraints in online advertising, we investigate single-parameter auction design for bidders with constraints on their Return On Investment (ROI) – a targeted minimum ratio between the obtained value and the payment. We focus on ex post ROI constraints, which require the ROI condition to be satisfied for every realized value profile. With ROI-constrained bidders, we first provide a full characterization of the allocation and payment rules of dominantstrategy incentive compatible (DSIC) auctions. In particular, we show that given any monotone allocation rule, the corresponding DSIC payment should be the Myerson payment with a rebate for each bidder to meet their ROI constraints. Furthermore, we also determine the optimal auction structure when the item is sold to a single bidder under a mild regularity condition. This structure entails a randomized allocation scheme and a first-price payment rule, which differs from the deterministic Myerson auction and previous works on ex ante ROI constraints. 

Keywords: Return on investment (ROI) · Mechanism design · Myerson auction. 

## 1 Introduction 

Online advertising auctions are a vital source of revenue for many IT companies, generating billions of dollars of revenue annually. In recent years, with tens of millions of ad auctions being conducted in real-time each day, this large-scale and complex market has prompted modern online advertising platforms to develop auto-bidding services, which allow the advertisers to set up high-level marketing goals for their ad campaigns and then bid on behalf of the advertisers. 

> ⋆ Z. Zheng is the corresponding author. 

2 H. Lv et al. 

In these auto-bidding scenarios, advertisers’ financial constraints such as budget and return on investment (ROI) constraints have become critical in auction design. While auctions for budget-constrained bidders have been extensively studied in the literature [22; 8; 19], research on auction design for bidders with ROI constraints is still in its nascent stage. The ROI constraints of advertisers require that the payment cannot be more than a certain fraction of the obtained advertising value. In other words, there is a targeted minimum ratio between the obtained value and the payment for an ROI-constrained bidder. Unlike budget constraints which set a hard limit on payment, ROI constraints establish a payment limit that is linearly related to the allocated value. Previous studies [16; 2] have demonstrated that ROI constraints align better with real-world empirical evidence than budget constraints, and it is the aim of this paper to explore how to design auctions with good incentive and revenue guarantees for ROI-constrained bidders. 

The existing literature on auction design for ROI-constrained bidders primarily focuses on ex ante ROI constraints, which requires an expected ROI with respect to the prior value distributions of bidders [16; 6]. This approach is suitable for advertisers who participate in a large number of auctions daily and are only concerned with their average spend per unit of value. However, in reality, most ad campaigns experience the “long-tail phenomenon” [9], which means they only receive dozens of or fewer clicks per day. Under these conditions, an auction with ex ante ROI guarantees may have a non-negligible probability of violating the ROI constraints of these ad campaigns over a day. Due to these reasons, in this work, we focus on the ex post or hard ROI constraints, which ensures that the auction respects the ROI constraints of bidders for any realized value profile. This is a stronger requirement compared to ex ante ROI constraints and addresses the limitation of current auction design methods. 

### 1.1 Our Results 

In this work, we examine the design of truthful and optimal auction design for ex post ROI-constrained bidders. We inherit the setting from the classic singleparameter mechanism design and consider the values of bidders as private information and the targeted ROIs as public information. In this single-parameter environment, the ROI constraints can be integrated into the objective function (see Section 2 for details), resulting in a transformed utility model: ui = Mivixi − pi, where ui represents the utility of bidder i, vi is the value, xi is the allocation quantity, and pi is the payment. Here Mi > 1 is the targeted ROI ratio, which differentiates this model from the classical quasilinear utility model. 

We first study the characterizations of truthful auctions with ROI-constrained bidders. Compared to Myerson’s characterization of truthful auctions in the single-parameter environment, we show that the monotonicity requirement of the allocation rule remains true for ex post ROI-constrained bidders, but the unique payment rule in [24] should be modified by subtracting a max term, which can be interpreted as a “rebate” equal to the largest “violation” of the Myerson payment to the ROI constraint for all lower valuations. This is a full characterization that 

Auction Design for Bidders with Ex Post ROI Constraints 3 

completely describes all truthful auctions with ROI-constrained bidders. This result can be proved using similar techniques from Myerson’s analysis. It can also be derived from the following alternative interpretation of the payment rule: note that the ROI-constrained bidder assigns a weight Mi > 1 to her obtained value vixi from the allocation, but not to her payment. To not violate the individual rationality (IR) condition, instead of applying a naive approach that charges the bidder Mi times the Myerson payment, we must iteratively apply the Myerson payment increment (multiplied by Mi) in small intervals and truncate the payment at the obtained value whenever necessary. 

Next, we turn our focus to the optimal (i.e. revenue-maximizing) auction design. The additional max term in our payment rule poses a significant challenge to the optimal auction design, since it is unclear how this term can be incorporated into a modified virtual valuation function as seen in previous literature. Instead, we concentrate on the case of selling a single item to a single bidder. Our main result suggests that under a mild regularity assumption known as decreasing marginal revenue (DMR)<sup>1</sup> , the optimal auction for selling to a single ex post ROI-constrained bidder employs a randomized scheme. More specifically, the allocation rule x(·) starts with a first-price interval, where the payment always matches the obtained value, until it reaches the highest allocation and x(·) becomes constant thereafter. This finding is in contrast to the classic Myerson auction [24] and previous results for bidders with ex ante ROI constraints, where the optimal auctions are always deterministic. It implies that similar to much literature on optimal mechanism design for multi-parameter settings, a slight generalization, such as the inclusion of the Mi term, in the single-parameter setting can lead to randomized optimal auctions. 

### 1.2 Related work 

There are two main threads of studies of auctions with ROI-constrained bidders. The first thread investigates how the bidding strategies of the bidders are affected by the ROI constraints in classic VCG or generalized second price (GSP) auctions [26; 7; 15; 27; 1; 18; 3]. The second thread, which our paper follows, focuses on the design of auctions with ROI-constrained bidders, which is of practical interest to many online advertising platforms [16; 6; 15; 20; 10; 28; 21; 5; 23]. In this line of study, the most related work to ours is [16], which showed empirically that a fraction of the buyers in online advertising are indeed ROI-constrained. They also took the first step towards revenue-maximizing auction design for bidders with ex ante ROI constraints. Note that ex ante ROI constraints only require the ROI conditions to be met in expectation and are strictly weaker than ex post ROI constraints. Another recent work [6] considered the scenario where either the value or the ROI constraint is private information of the bidder. They used 

> 1 DMR requires the marginal revenue, vf (v) + F (v) − 1 to be non-decreasing in the value space. This is different from the usual definition of regularity which requires the same monotonicity but in the quantile space. Please see the related work section for a more detailed discussion of their differences and more related works. 

4 H. Lv et al. 

a similar utility function as ours, but still focus on the concept of ex ante ROI. Unlike these works, we concentrate on ex post ROI constraints, which provide a hard ROI guarantee for bidders in every possible value realization. In [12; 4], the authors considered ex post ROI constraints in multiple stages, and assumed that each bidder maintains a fixed bid multiplier among stages, which leads to completely different problems from ours. 

One particular line of research focuses on requirements of truthfulness for ex post ROI constraints. Cavallo et al. studied the same utility function as ours in [10, Appendix A], and investigated the corresponding payment rules. The main difference is that, they limited their focus on deterministic mechanisms for bidders with identical ROI constraints, while we consider a more general single-parameter setting in the randomized mechanism domain. Li et al. [20] proposed a condition on truthfulness of the ROI information, based on which they provided a mechanism framework using tools from control theory. They took the ROI constraints as private information, instead of the value, which leads to a substantially different problem from ours. 

The DMR assumption used in our optimal auction characterization has been widely discussed in the literature. It means that the function ψ(v) ≜ vf (v) + F (v) − 1 is non-decreasing, or equivalently v · (1 − F (v)), which is the expected revenue of selling the item at price p, is concave, and this is where the name of this condition comes from. Intuitively, many commonly used distribution functions satisfy this assumption, e.g., uniform distributions, and any distribution of finite support and monotone non-decreasing density. The DMR condition was first proposed in [11] for bidders with budget constraints. In [14], the authors found that the DMR condition is more natural in their setting than the traditionally used notion of regularity [24], since DMR precisely removes the requirement of ironing in the value space, instead of in the quantile space as in [24]. In [13], DMR was discussed comprehensively, and the authors showed that the optimal mechanism is deterministic under the DMR condition in a multi-unit setting with private demands. We refer the reader to their work for concrete examples and more discussion. 

## 2 Preliminaries 

We consider a general single-parameter auction environment, which consists of a seller and n bidders N = {1, 2, ..., n}. Each bidder i has a private valuation ti per unit of the good. We represent xi as the quantity of the allocated good to bidder i and pi as the payment of bidder i. Without loss of generality, we assume the maximum possible allocation is x<sup>max</sup> i = 1 and the good is indivisible, that is, xi denotes the probability of bidder i receiving the good. Besides the allocated value, each bidder also has a return on investment (ROI) constraint Mi, as public information<sup>2</sup> , which specifies the minimum targeted ratio between her obtained value and the payment. We assume 1 < Mi < +∞ in this work. 

> 2 This setting is practical and prevalent in practice, e.g., in online advertising, the targeted ROI typically remains the same over a certain period. 

Auction Design for Bidders with Ex Post ROI Constraints 

5 

We note that the ROI constraint is considered in an ex post measure, i.e., it requires that<sup>ti</sup> p<sup>x</sup> i<sup>i≥Mistrictlyholdsintheoutcomeofeveryauctioninstance.</sup> Note that the same model is also adopted in [10, appendix A]. 

With the above definitions, the utility of bidder i is given by 


![](assets/wine23/wine23.pdf-0005-04.png)


It is worth noting that this is the standard quasilinear utility model with the addition of the ROI constraint. We can further define 


![](assets/wine23/wine23.pdf-0005-06.png)


which could be interpreted as the maximum willingness-to-pay of the bidder i per unit of the good. Then, we can rewrite the utility function as 


![](assets/wine23/wine23.pdf-0005-08.png)


One can observe that, as Mi is a public constant, vi and ti are completely interchangeable. To avoid confusion, we use the term value to represent vi, and initial value to represent ti in the following discussion. Each value vi is independently drawn from a probability distribution Fi : [0, vmax] → [0, 1], with a continuous probability density function fi. While the distributions Fi’s are common knowledge, the exact value vi is known only to the bidder i. We denote v as the value profile of all bidders, and v−i as that of all bidders except bidder i. 

In an auction, each bidder reports her value as bi, which is not necessarily equal to vi. We define b and b−i similarly as the notations of v and v−i. Based on the reported bids, an auction mechanism consists of an allocation rule xi(bi, b−i), mapping the bid profile to the allocated quantity to each bidder i, and a payment rule pi(bi, b−i), mapping the bid profile to the payment for each bidder. When clear from context, we will omit b−i in the mappings. We also use ui(bi, vi) to represent the utility of bidder i who has value vi and bid bi. In the following discussion, we assume that the allocation rule xi(·) is always right-differentiable, and there are finite non-differentiable points. When xi(·) is non-continuous at v, let xi(v) = limz→v+ xi(z). 

We are interested in auctions that are dominant-strategy incentive compatible (DSIC) and individually rational (IR). 

Definition 1 (Dominant-Strategy Incentive Compatibility, DSIC). A mechanism is dominant-strategy incentive compatible if and only if 


![](assets/wine23/wine23.pdf-0005-13.png)


Definition 2 (Individual Rationality, IR). A mechanism is individually rational if and only if 

ui(vi, vi) ≥ 0, ∀vi, b−i, i ∈ N . 

- 6 H. Lv et al. 

For ease of notation, we use truthfulness to represent the properties of both DSIC and IR in the following sections. In addition, for truthful auctions, we do not distinguish vi and bi hereinafter. 

The revenue of a truthful auction is defined as 


![](assets/wine23/wine23.pdf-0006-03.png)


The aim of this work is to characterize both truthful and revenue-maximizing (optimal) auctions with ex post ROI-constrained bidders. 

## 3 Characterize the Structure of DSIC Auctions 

In this section, we present characterizations of the DSIC auctions with ex post ROI constraints. These results generalize the classical Myerson’s Lemma [24] for the traditional utility model (i.e., Mi = 1), which states that in the singleparameter environment, a mechanism is DSIC if and only if its allocation rule is monotone and the payment scheme follows a unique rule. 

Lemma 1 (Myerson’s Lemma [24]). For traditional bidders with Mi = 1, a single-parameter mechanism is DSIC if and only if: 

- [Monotone Allocation Rule] the allocation rule is monotonically non-decreasing, i.e., xi(v) ≤ xi(v<sup>′</sup> ) for all v < v<sup>′</sup> and bidder i; 

- [Unique Payment Rule] for each monotonically non-decreasing allocation rule xi(·), and pi(0) = 0, the payments are given by 


![](assets/wine23/wine23.pdf-0006-10.png)


Clearly, these results cannot be directly applied to the ROI-constrained bidders, because the payment derived from Myerson’s Lemma may violate the ROI constraints. The main result in this section is a complete characterization of the DSIC mechanisms with ROI-constrained bidders. We will see that the monotonicity condition for the allocation remains the same, but the payment rule needs to be modified appropriately to accommodate the ROI constraints. 

Theorem 2 (Characterization). For ex post ROI-constrained bidders, a singleparameter mechanism is DSIC if and only if: 

- [Monotone Allocation Rule] the allocation rule is monotonically non-decreasing, i.e., xi(v) ≤ xi(v<sup>′</sup> ) for all v < v<sup>′</sup> and bidder i; 

- [Unique Payment Rule] for each monotonically non-decreasing allocation rule xi(·), and pi(0) = 0, the payments are given by 


![](assets/wine23/wine23.pdf-0006-15.png)


where p�i is the Myerson payment given in (3). 

Auction Design for Bidders with Ex Post ROI Constraints 7 

We can interpret this characterization from two perspectives: First, from the perspective of the initial value ti of bidder i, it suggests that compared to the classic Myerson auction, an ROI-constrained bidder with value v will need to pay the initial Myerson payment Mip�i(v) (recall that ti = Mivi), minus a “rebate” which equals to the largest “violation” of the Myerson payment to the ROI requirement when the bidder’s valuation is no more than v. 

Second, from the perspective of the value vi, since the ROI-constrained bidder assigns a weight Mi > 1 to her obtained value from the allocation, but not to her payment, a naive application that charges the bidder Mi times of the Myerson payment may violate the IR constraint. Therefore, we need to iteratively apply the Myerson payment increment (multiplied by Mi) in small intervals and truncate the payment at the value whenever necessary. These two perspectives are mathematically equivalent, and we adopt the second perspective in the following for exposition convenience. 

Next, before proving this theorem, some observations are immediate from this characterization. We defer the proof of these observations to Appendix A. 

### Proposition 1. 

1. We always have pi(v) ≤ vxi(v) and pi(v) ≤ Mip�i(v) for any bidder i and value v in DSIC mechanisms. 

2. The payment function pi(·) is monotonically non-decreasing for any bidder i in DSIC mechanisms. 

Now we proceed to prove Theorem 2. The proof consists of showing the following claims in sequence. It is not difficult to see that these three claims together imply Theorem 2. 

1. For ex post ROI-constrainted bidders, if a mechanism is DSIC, then the allocation rule must be monotonically non-decreasing. 

2. Any monotonically non-decreasing allocation rule xi(·) with the payment rule given in (4) produces a DSIC mechanism. 

3. Given any monotone allocation rule x(·), the payment rule p(·) such that (x, p) is DSIC, if exists, must be unique. 

The analyses of steps (1) and (3) are very similar to the proof of the original Myerson’s Lemma, and we defer the details to Appendix B and C. Next, we prove step (2). When clear from context, we will drop the subscript i in xi(·), pi(·), ui(·) and Mi as shorthand in the following proofs. 

Proof of Step (2). Consider a bidder i with private valuation v and fix the other bids b−i. We examine the utilities of bidder i when she bids her true valuation and when she bids some different value v<sup>′̸</sup> = v. Consider two cases. 

- When v<sup>′</sup> < v, we have max0≤z≤v{M �p(z) − zx(z)} ≥ max0≤z≤v<sup>′</sup> {M �p(z) − zx(z)}, which implies 

p(v) − p(v<sup>′</sup> ) ≤ M (p�(v) − p�(v<sup>′</sup> )). 

8 H. Lv et al. 

This inequality effectively removes the max term in the payment formula (4) and reduces the problem to that with the Myerson payment. This allows us to apply the standard argument for the Myerson auction to show the DSIC property of our mechanism. We show the analysis below for completeness. We can compute the utility difference of bidder i when she bids v and v<sup>′</sup> , and get 


![](assets/wine23/wine23.pdf-0008-02.png)


where the second equality is by plugging in the Myerson payment formula (3). This means bidder i has no incentive to misreport her valuation v as v<sup>′</sup> in this case. 

- When v<sup>′</sup> > v, we examine max0≤z≤v{M �p(z)−zx(z)} and max0≤z≤v′ {M �p(z)− zx(z)}. There are two possibilities: 

   - If these two terms are equal, then we can apply the same argument as in the previous case (and also as in the Myerson auction analysis) to prove the DSIC property. We omit the details here. 

   - If max0≤z≤v{M �p(z) − zx(z)} < max0≤z≤v′ {M �p(z) − zx(z)}, this means arg max0≤z≤v′ {M �p(z) − zx(z)} = v<sup>∗</sup> > v. Then at valuation v<sup>′</sup> , we should have 


![](assets/wine23/wine23.pdf-0008-07.png)


That is to say, when reporting v<sup>′</sup> , the payment of bidder i will be greater than the value she obtains (which is vx(v<sup>′</sup> )), therefore violating the IR condition. So bidder i has no incentive to misreport as v<sup>′</sup> in this case. 

Auction Design for Bidders with Ex Post ROI Constraints 

9 

## 4 Optimal Auction Design for a Single Bidder 

Having obtained the precise characterization of the allocation rule and payment function in the setting with ROI constraints, we now turn to the revenue maximization auction design. Recall that in the Myerson auction [24] and previous works in the ex ante ROI constraints setting [6; 16], the revenue maximization problem is reduced to the problem of maximizing (modified) virtual welfare. Unfortunately, with ex post ROI constraints, the payment function characterization (4) involves an additional max term compared to the Myerson payment, and it is unclear how to incorporate this term into a modified virtual valuation formulation. We present the following simple example with a single bidder to demonstrate that, unlike the Myerson auction, the allocation that maximizes the virtual welfare may no longer be optimal with ROI-constrained bidders. 


![](assets/wine23/wine23.pdf-0009-04.png)


<!-- Start of picture text -->
x(v) x(v)<br>p(v) = vx(v)<br>1 1<br>p(v) = 2 1 p(v) = 4 3<br>0 1 1 v 0 3 1 v<br>2 4<br>(a) The Myerson auction (b) The optimal auction for ROI-<br>constrained bidders<br><!-- End of picture text -->

Fig. 1: The Myerson auction and the optimal auction for one bidder with uniform value distribution over [0, 1] and M = 2. 

Example 1. Consider selling a single item to a single bidder with ROI constraint M = 2 and valuation for the item v following a uniform distribution U [0, 1]. If we disregard the ROI constraint ( i.e., let M = 1), the virtual valuation of this bidder is φ(v) = 2v − 1, and the optimal Myerson auction, as shown in Fig. 1a, sells the item at price p = 2<sup>1withtheexpectedrevenueof1</sup> 2<sup>·1</sup> 2<sup>=</sup> 4<sup>1.</sup> 

However, with the ROI constraint M = 2 in presence, this allocation rule (x(v) = 0 when v < 1/2 and x(v) = 1 otherwise) is no longer optimal. As shown in Fig. 1b, the optimal auction, which will be proved in Theorem 5 later in this section, is a randomized auction with the allocation rule given by 


![](assets/wine23/wine23.pdf-0009-08.png)


This allocation rule would generate an expected revenue of 83<sup>,whichishigher</sup> than<sup>1</sup> 4<sup>.</sup> 

10 H. Lv et al. 

This example already highlights an important feature of the optimal auction with ROI constraints: the allocation and payment may be randomized, even in the simple setting with a single bidder and uniform value distribution. It also suggests that it is difficult to follow the Myerson auction regime and reduce the revenue maximization problem to a welfare maximization problem with some modified virtual valuation. It seems a very challenging problem to obtain a characterization for the optimal auction in this setting. Instead, in this section we focus on the special case when the item is sold to a single bidder. As we will show in the following analysis, this is already a nontrivial and interesting problem to design an optimal auction for a single bidder. 

First, we show that with a single ROI-constrained bidder, the max term in the payment formula (4) would be always 0, reducing the payment rule (4) to the standard Myerson payment (multiplied by a factor of M ). We defer the proof to Appendix D. 

Lemma 3. In the optimal auction with a single ROI-constrained bidder, let (x, p) be the revenue-maximizing auction, then we have M �p(v) ≤ v · x(v) for any value v ∈ [0, vmax]. In other words, max0≤z≤v{M �p(z) − zx(z)} = 0 (which is achieved at z = 0) for all v ∈ [0, vmax], and the payment rule reduces to p(v) = M �p(v). 

With Lemma 3 at hand, it seems with a single bidder, we are back to the classic Myerson regime, where the revenue maximization problem can be converted to a welfare maximization problem with respect to the virtual valuation. That is, recall from the Myerson’s theorem [24], we have 


![](assets/wine23/wine23.pdf-0010-05.png)


where φ(v) = �v −<sup>1−</sup> f<sup>F</sup> (v<sup>(</sup> )<sup>v)</sup> � is the virtual valuation. However, we still have the additional constraint that M �p(v) ≤ v · x(v) for every v. This restricts our allocation space and turns the problem into a constrained welfare maximization problem. 

In the following, we provide some further characterizations on the structure of the optimal auction with a single ROI-constrained bidder. We defer the proof to Appendix E. 

Lemma 4. With a single ROI-constrained bidder, there always exists a revenuemaximizing auction such that for any valuation v, at least one of the following statements holds: 

– the derivative of allocation rule at the valuation v exists, and x<sup>′</sup> (v) = 0; 

– the payment follows the first-price rule, i.e., p(v) = vx(v). 

Lemma 4 allows us to focus on auctions with a very specific structure: as long as the allocation is not constant, it always follows the first-price payment rule. In particular, combining with Lemma 3, it implies whenever x<sup>′</sup> (v) exists and x<sup>′</sup> (v) > 0, we always have p = vx(v) = M �p(v). 

Auction Design for Bidders with Ex Post ROI Constraints 11 

Next, we want to obtain a further characterization of the optimal auction with a single bidder. However, to do this would require us to make a mild assumption on the value distribution of the bidder, which is known as the Decreasing Marginal Revenue (DMR) condition by [13]. 

Definition 3 (Decreasing Marginal Revenue, DMR). The value distribution of a bidder satisfies the condition of decreasing marginal revenue if and only if the function 


![](assets/wine23/wine23.pdf-0011-03.png)


is monotonically non-decreasing. 

Note that ψ(v) being non-decreasing is equivalent to the fact that v·(1−F (v)), which is the expected revenue of selling the item at price p, being concave, and this is where the name of this condition comes from. Intuitively, many commonly used distribution functions satisfy this assumption, e.g., uniform distributions, and any distribution of finite support and monotone non-decreasing density. The DMR condition is closely related to the regularity condition but they are incompatible<sup>3</sup> . We refer the reader to [13] for concrete examples and more discussion. 

With the assumption of DMR, the optimal auction exhibits an even simpler structure than what is described in Lemma 4, namely that there exist only two intervals in the optimal auction: interval of (0, D) with x<sup>′</sup> (v) > 0 and interval of (D, vmax) with x<sup>′</sup> (v) = 0, where D is a threshold valuation between them. This leads to our main theorem in this section, which characterizes the optimal allocation rule and payment rule for a single ROI-constrained bidder. 

Theorem 5. The optimal auction for a single ex post ROI-constrained bidder with a DMR value distribution over [0, vmax] is as follows: 

– when v < D, the allocation is given by 


![](assets/wine23/wine23.pdf-0011-09.png)


and the payment follows the first-price rule, i.e., p(v) = vx(v); 

– when v ≥ D, the allocation rule is x(v) = 1, and the payment is given by p(v) = D. 

Here D is a threshold valuation given as follows: 


![](assets/wine23/wine23.pdf-0011-13.png)


This theorem provides an important insight that the optimal auction in the ROI-constrained setting is a randomized mechanism. Note that Myerson’s optimal auction in the single-parameter setting is deterministic, but a decent body 

> 3 The regularity condition is equivalent to the expected revenue being concave in the quantile space, while the DMR condition means the expected revenue is concave in the value space. 

12 H. Lv et al. 

of works has shown that many generalizations to multi-parameter settings will lead to randomized optimal auctions [25; 17]. Theorem 5 indicates that, even in the single-parameter environment, a slight generalization with an ROI constraint to the bidder will also lead to a randomized optimal auction. 

We prove the theorem via the following steps. First, we derive the allocation of an optimal auction in an interval (0, v<sup>∗</sup> ) when x<sup>′</sup> (v) is always positive in that interval. Then, we show in Lemma 6 that there exist only two intervals in the optimal auction: interval of (0, D) with x<sup>′</sup> (v) > 0 and interval of (D, vmax) with x<sup>′</sup> (v) = 0. Finally, we will compute the optimal threshold valuation D between these two intervals. 

Proposition 2. If for some v<sup>∗</sup> ∈ (0, vmax], we have x<sup>′</sup> (v) > 0 for all v ∈ (0, v<sup>∗</sup> ) in an optimal auction, then x(·) is continuous at v<sup>∗</sup> , and the allocation rule x(v) for all v ∈ [0, v<sup>∗</sup> ] is given as: 


![](assets/wine23/wine23.pdf-0012-04.png)


Proof. We first assume x(·) is continuous at v<sup>∗</sup> , and we will prove later that, if it is discontinuous, we can improve the revenue without violating the DSIC property. By Lemma 3 and Lemma 4, we get that for all valuations v ∈ [0, v<sup>∗</sup> ], M �p(v) − vx(v) = 0 always holds, that is, 


![](assets/wine23/wine23.pdf-0012-06.png)


After transposition and derivation, this translates to 


![](assets/wine23/wine23.pdf-0012-08.png)


By solving this differential equation with the value of x(v<sup>∗</sup> ) at valuation v<sup>∗</sup> , we can get 


![](assets/wine23/wine23.pdf-0012-10.png)


Next, if x(·) is discontinuous at v<sup>∗</sup> , we need to replace x(v<sup>∗</sup> ) in (5) with x(v<sup>∗−</sup> ), i.e., the left limit of x(·) at v<sup>∗</sup> (recall that we denote x(v<sup>∗</sup> ) as the right limit when it is discontinuous). Since x(v<sup>∗−</sup> ) < x(v<sup>∗</sup> ), we can observe that directly using (5) as the allocation rule will increase the revenue without violating the DSIC property, which also makes x(·) continuous at v<sup>∗</sup> . This concludes the proof. 

Lemma 6. For a single ROI-constrained bidder with DMR value distribution, if there exist intervals with x<sup>′</sup> (v) = 0 in an optimal auction, then there is exactly one such interval, and it appears in the highest value region. 

Proof. Assume by contradiction that there exist multiple intervals with x<sup>′</sup> (v) = 0 in an optimal auction. Pick (v, ¯v) to be the first such interval. That is, we have x<sup>′</sup> (v) > 0 for all v ∈ (0, v), x<sup>′</sup> (v) = 0 for all v ∈ (v, ¯v), and v¯ < vmax. 

Auction Design for Bidders with Ex Post ROI Constraints 13 

First, we must have v > 0. That is, the allocation rule cannot start with a flat interval. To see why this is true, assume otherwise that v = 0. We focus on a point v<sup>′</sup> = v¯ + δ in the next interval for a sufficiently small δ > 0 such that v<sup>′</sup> < M ¯v. Then there are two cases: (1) x<sup>′</sup> (v<sup>′</sup> ) = 0 and (2) x<sup>′</sup> (v<sup>′</sup> ) is strictly positive. In the first case, we will have x(¯v) > 0, and the Myerson price at v¯ will be p�(¯v) = v¯ · x(¯v) < M �p(¯v), which directly contradicts Lemma 3. In the second case, we look at the payment p(v<sup>′</sup> ) at point v<sup>′</sup> . Note that since x<sup>′</sup> (v) > 0, by Lemma 3 and Lemma 4, we should have M �p(v<sup>′</sup> ) = v<sup>′</sup> x(v<sup>′</sup> ). But this cannot happen because 


![](assets/wine23/wine23.pdf-0013-02.png)


Knowing v > 0, by Proposition 2, we know x(·) is continuous at v, and the allocation in [0, v] is given as: 


![](assets/wine23/wine23.pdf-0013-04.png)


Next, combined with p(¯v) = vx¯ (¯v), we have M �p(¯v) − vx¯ (¯v) = M �p(v) − vx(v), that is, 


![](assets/wine23/wine23.pdf-0013-06.png)


In order to argue that allocation rule x(·) is not revenue-maximizing, we construct a new allocation rule as 


![](assets/wine23/wine23.pdf-0013-08.png)


That is, we replace the first price interval [0, v] and the flat interval [v, ¯v] in x(·) with a single first-price interval [0, ¯v] in x¯(·). Comparing the two allocation rules x(·) and x¯(·), we first note from Lemma 3 and Lemma 4 that p(¯v) = M �p(¯v) = vx¯ (¯v) = v¯x¯(¯v), which indicates that 


![](assets/wine23/wine23.pdf-0013-10.png)


because both sides equal to vx¯ (¯v)(M − 1)/M . Next, we have for v ∈ [0, v], 


![](assets/wine23/wine23.pdf-0013-12.png)


14 H. Lv et al. 

Since v only appears in the first term, x¯(v) − x(v) must be constantly positive or negative in (0, v], determined by the last term. Combined with (8) and x<sup>′</sup> (v) = 0, ∀v ∈ (v, ¯v), we know it is constantly negative, i.e., x¯(v) < x(v) for all v ∈ (0, v]. Therefore, there exists a threshold v<sup>∗</sup> ∈ (v, ¯v) such that x(v) > x¯(v) for all v ∈ [0, v<sup>∗</sup> ) and x(v) ≤ x¯(v) for all v ∈ [v<sup>∗</sup> , ¯v). Combining this with Equation (8), we have 


![](assets/wine23/wine23.pdf-0014-02.png)


Next, for any allocation rule x(·), we denote 


![](assets/wine23/wine23.pdf-0014-04.png)


and we can compare the revenue generated from x(·) and x¯(·) in the interval [0, ¯v]: 


![](assets/wine23/wine23.pdf-0014-06.png)


Finally, we can see that this difference is always negative due to Equation (9) and the fact that ψ(·) is non-decreasing.<sup>4</sup> Fig. 2 demonstrates the idea of this argument. 


![](assets/wine23/wine23.pdf-0014-08.png)


<!-- Start of picture text -->
x(v)<br>x¯(v)<br>0 v v ∗ v¯ v<br><!-- End of picture text -->

Fig. 2: An illustration for the proof of Lemma 6 with M = 3. The blue line denotes an allocation rule x(·) with x<sup>′</sup> (v) = 0 in (v, ¯v) where v¯ < vmax, and x(v) for v ∈ [0, v) is computed by Proposition 2. The red line denotes our constructed allocation rule x¯(·) as given in (7). The point v<sup>∗</sup> denotes the intersection of x(·) and x¯(·). By Equation (9) we have the areas of the two shadowed regions are the same. Furthermore, as ψ(·) is non-decreasing, we can conclude that x¯(·) leads to a higher revenue than x(·). 

Therefore, we conclude that x¯(·) generates a higher revenue than x(·), contradicting the fact that (x, p) is an optimal auction. This completes the proof. 

> 4 We omit an ill-defined special case where ψ(v) = 0, ∀v ∈ [0, ¯v], since in such case ψ(v) will be infinity when v → 0. 

Auction Design for Bidders with Ex Post ROI Constraints 

15 

We now proceed to complete the proof of Theorem 5. 

Proof of Theorem 5. By Lemma 6, we know x<sup>′</sup> (v) > 0 for all valuations v ∈ (0, D) and x<sup>′</sup> (v) = 0 for all valuations v ∈ (D, vmax). First, we have x(D) = 1, since otherwise, the revenue could be improved by setting x(v) = 1 for all v ∈ [D, vmax]. Next, we find the optimal threshold D<sup>∗</sup> that maximizes the overall revenue. By Proposition 2, the allocation rule for valuations v ∈ [0, D] is 


![](assets/wine23/wine23.pdf-0015-04.png)


And the overall revenue is 


![](assets/wine23/wine23.pdf-0015-06.png)


In order to maximize this revenue, we compute its derivative 


![](assets/wine23/wine23.pdf-0015-08.png)


Looking at this derivative, we see that the term − M1−1<sup>· D−</sup> MM−1 is always neg1 ative and v M −1 is always positive. Furthermore, we have ψ(0) = −1 < 0 and ψ(vmax) > 0. By the DMR condition, ψ(·) is non-decreasing. Therefore, we have the following two cases: 

1 1 – If �0vmax ψ(v)v M −1 dv > 0, then by letting �0D<sup>∗</sup> ψ(v)v M −1 dv = 0, the revenue will increase with D until D<sup>∗</sup> and then decrease. Therefore, the optimal solution is achieved at D = D<sup>∗</sup> . 

1 – If �0vmax ψ(v)v M −1 dv ≤ 0, then the revenue will always increase with D until vmax. Therefore, the optimal solution is achieved at D = vmax. 

This completes the proof. 

## 5 Conclusion 

In this paper we discuss optimal auction design for bidders who have ex post ROI constraints. We provide characterizations for DSIC auctions and optimal auctions with a single bidder in this setting. We show that the optimal auction may entail a randomized allocation scheme even in the simple single-bidder setting. 

There are several important open questions left in this model. The first and foremost one is to characterize the optimal auction with a single item and multiple ROI-constrained bidders. As we have discussed in the paper, this would require us to go beyond the virtual welfare maximization regime in the Myerson auction setting. We believe such characterization could shed light on the mechanism design for bidders with non-quasilinear utility functions and provide useful 

16 H. Lv et al. 

insights for practical applications such as online advertising. Another direction is to study ex post ROI constraints when the target ratio Mi is also private information of bidder i. This brings the problem to the domain of multidimensional mechanism design, which is often challenging in the mechanism design literature. Here one possible approach is to identify conditions under which some “simple” and deterministic auctions are optimal or close to optimal. 

## 6 Acknowledgement 

We thank Hu Fu, Yiqing Wang, Yidan Xing, Xiangyu Liu and anonymous reviewers for their insightful and helpful suggestions. This work was supported in part by National Key R&D Program of China No. 2021YFF0900800, in part by China NSF grant No. 62220106004, 62322206, 62132018, 62272307, 61972254, 62025204, 62302267, in part by the Natural Science Foundation of Shandong (No. ZR202211150156, ZR2021LZH006), in part by Alibaba Group through Alibaba Innovative Research Program, and in part by Tencent Rhino Bird Key Research Project. The opinions, findings, conclusions, and recommendations expressed in this paper are those of the authors and do not necessarily reflect the views of the funding agencies or the government. 

## Bibliography 

- [1] Aggarwal, G., Badanidiyuru, A., Mehta, A.: Autobidding with constraints. In: International Conference on Web and Internet Economics. pp. 17–30. Springer (2019) 

- [2] Auerbach, J., Galenson, J., Sundararajan, M.: An empirical analysis of return on investment maximization in sponsored search auctions. In: Proceedings of the 2nd International Workshop on Data Mining and Audience Intelligence for Advertising. pp. 1–9 (2008) 

- [3] Babaioff, M., Cole, R., Hartline, J., Immorlica, N., Lucier, B.: Non-quasilinear agents in quasi-linear mechanisms. Leibniz international proceedings in informatics 185 (2021) 

- [4] Balseiro, S., Deng, Y., Mao, J., Mirrokni, V., Zuo, S.: Robust auction design in the auto-bidding world. Advances in Neural Information Processing Systems 34, 17777–17788 (2021) 

- [5] Balseiro, S., Golrezaei, N., Mirrokni, V., Yazdanbod, S.: A black-box reduction in mechanism design with private cost of capital. Available at SSRN 3341782 (2019) 

- [6] Balseiro, S.R., Deng, Y., Mao, J., Mirrokni, V.S., Zuo, S.: The landscape of auto-bidding auctions: Value versus utility maximization. In: Proceedings of the 22nd ACM Conference on Economics and Computation. pp. 132–133 (2021) 

- [7] Borgs, C., Chayes, J., Immorlica, N., Jain, K., Etesami, O., Mahdian, M.: Dynamics of bid optimization in online advertisement auctions. In: Proceedings of the 16th international conference on World Wide Web. pp. 531–540 (2007) 

Auction Design for Bidders with Ex Post ROI Constraints 17 

- [8] Borgs, C., Chayes, J., Immorlica, N., Mahdian, M., Saberi, A.: Multi-unit auctions with budget-constrained bidders. In: Proceedings of the 6th ACM Conference on Electronic Commerce. pp. 44–51 (2005) 

- [9] Brynjolfsson, E., Hu, Y., Simester, D.: Goodbye pareto principle, hello long tail: The effect of search costs on the concentration of product sales. Management Science 57(8), 1373–1386 (2011) 

- [10] Cavallo, R., Krishnamurthy, P., Sviridenko, M., Wilkens, C.A.: Sponsored search auctions with rich ads. In: Proceedings of the 26th International Conference on World Wide Web. pp. 43–51 (2017) 

- [11] Che, Y.K., Gale, I.: Standard auctions with financially constrained bidders. The Review of Economic Studies 65(1), 1–21 (1998) 

- [12] Deng, Y., Mao, J., Mirrokni, V., Zuo, S.: Towards efficient auctions in an auto-bidding world. In: Proceedings of the Web Conference 2021. pp. 3965– 3973 (2021) 

- [13] Devanur, N.R., Haghpanah, N., Psomas, C.A.: Optimal multi-unit mechanisms with private demands. In: Proceedings of the 2017 ACM Conference on Economics and Computation. pp. 41–42 (2017) 

- [14] Fiat, A., Goldner, K., Karlin, A.R., Koutsoupias, E.: The fedex problem. In: Proceedings of the 2016 ACM Conference on Economics and Computation. pp. 21–22 (2016) 

- [15] Golrezaei, N., Jaillet, P., Liang, J.C.N., Mirrokni, V.: Bidding and pricing in budget and roi constrained markets. arXiv preprint arXiv:2107.07725 (2021) 

- [16] Golrezaei, N., Lobel, I., Paes Leme, R.: Auction design for roi-constrained buyers. In: Proceedings of the Web Conference 2021. pp. 3941–3952 (2021) 

- [17] Hart, S., Reny, P.J.: Maximal revenue with multiple goods: Nonmonotonicity and other observations. Theoretical Economics 10(3), 893–922 (2015) 

- [18] Heymann, B.: Cost per action constrained auctions. In: Proceedings of the 14th Workshop on the Economics of Networks, Systems and Computation. pp. 1–8 (2019) 

- [19] Laffont, J.J., Robert, J.: Optimal auction with financially constrained buyers. Economics Letters 52(2), 181–186 (1996) 

- [20] Li, B., Yang, X., Sun, D., Ji, Z., Jiang, Z., Han, C., Hao, D.: Incentive mechanism design for roi-constrained auto-bidding. arXiv preprint arXiv:2012.02652 (2020) 

- [21] Li, J., Tang, P.: Auto-bidding equilibrium in roi-constrained online advertising markets. arXiv preprint arXiv:2210.06107 (2022) 

- [22] Malakhov, A., Vohra, R.V.: Optimal auctions for asymmetrically budget constrained bidders. Review of Economic Design 12(4), 245–257 (2008) 

- [23] Mehta, A.: Auction design in an auto-bidding setting: Randomization improves efficiency beyond vcg. In: Proceedings of the ACM Web Conference 2022. pp. 173–181 (2022) 

- [24] Myerson, R.B.: Optimal auction design. Mathematics of operations research 6(1), 58–73 (1981) 

- [25] Pavlov, G.: Optimal mechanism for selling two goods. The BE Journal of Theoretical Economics 11(1) (2011) 

- 18 H. Lv et al. 

- [26] Szymanski, B.K., Lee, J.S.: Impact of roi on bidding and revenue in sponsored search advertisement auctions. In: Second Workshop on Sponsored Search Auctions. pp. 1–8 (2006) 

- [27] Tillberg, E., Marbach, P., Mazumdar, R.: Optimal bidding strategies for online ad auctions with overlapping targeting criteria. vol. 4, pp. 1–55. ACM New York, NY, USA (2020) 

- [28] Wilkens, C.A., Cavallo, R., Niazadeh, R.: Gsp: the cinderella of mechanism design. In: Proceedings of the 26th International Conference on World Wide Web. pp. 25–32 (2017) 

Auction Design for Bidders with Ex Post ROI Constraints 19 

## A Proof of Proposition 1 

Proof. First, we have Mip�i(0) − 0 · xi(0) = 0 since xi(0) = 0 and pi(0) = 0. Then we can observe that 


![](assets/wine23/wine23.pdf-0019-03.png)


Therefore, pi(v) ≤ Mip�i(v). Similarly, we have 


![](assets/wine23/wine23.pdf-0019-05.png)


hence 


![](assets/wine23/wine23.pdf-0019-07.png)


For the second statement, we prove that for any values v < v<sup>′</sup> ∈ [0, vmax], pi(v) ≤ pi(v<sup>′</sup> ). we consider the following two cases: 

– When 


![](assets/wine23/wine23.pdf-0019-10.png)


we have 


![](assets/wine23/wine23.pdf-0019-12.png)



![](assets/wine23/wine23.pdf-0019-13.png)


we denote 


![](assets/wine23/wine23.pdf-0019-15.png)


Then we have that 


![](assets/wine23/wine23.pdf-0019-17.png)


and 


![](assets/wine23/wine23.pdf-0019-19.png)


By the analysis of the above case, we have 


![](assets/wine23/wine23.pdf-0019-21.png)


20 H. Lv et al. 

## B Proof of Monotone Allocation Rule (Step 1 of Theorem 2) 

Lemma 7 (Monotone Allocation Rule). For ex post ROI-constrained bidders, if a mechanism is DSIC, then the allocation rule is monotonically non-decreasing, that is, xi(v) ≤ xi(v<sup>′</sup> ) for all v < v<sup>′</sup> and bidder i. 

Before the proof, we first present elementary inequalities derived from the property of truthfulness for ex post ROI-constrained bidders. 

Given values v, v<sup>′</sup> with v < v<sup>′</sup> , by the truthfulness requirement, when a bidder i with value v misreports v<sup>′</sup> , we have 


![](assets/wine23/wine23.pdf-0020-05.png)


or 


![](assets/wine23/wine23.pdf-0020-07.png)


Similarly, considering bidder i with value v<sup>′</sup> misreports v, we obtain that 


![](assets/wine23/wine23.pdf-0020-09.png)


or 


![](assets/wine23/wine23.pdf-0020-11.png)


One can observe that (14) contradicts the IR requirement since pi(v) ≤ vxi(v) < v<sup>′</sup> xi(v). Hence, in a truthful mechanism, (13) must hold, and at least one of (11) and (12) holds. On the basis of this elementary analysis, we now prove Lemma 7. 

Proof. We prove the monotonicity by contradiction. Let v < v<sup>′</sup> , we assume xi(v) > xi(v<sup>′</sup> ) in a truthful mechanism. Then we prove that (11) and (13) are not compatible. By (13), we get 


![](assets/wine23/wine23.pdf-0020-14.png)


Similarly, by (11), we obtain 


![](assets/wine23/wine23.pdf-0020-16.png)


Combining (15) and (16), we have Miv<sup>′</sup> · (xi(v) − xi(v<sup>′</sup> )) ≤ Miv · (xi(v) − xi(v<sup>′</sup> )). However, since xi(v) > xi(v<sup>′</sup> ) and v<sup>′</sup> > v, we can derive a contradiction. 

Next, we continue to prove that (12) and (13) are not compatible. By the IR property, we have 


![](assets/wine23/wine23.pdf-0020-19.png)


Combining (12), (13), and (17), we obtain 


![](assets/wine23/wine23.pdf-0020-21.png)


that is, 


![](assets/wine23/wine23.pdf-0020-23.png)


As we have xi(v) > xi(v<sup>′</sup> ) and v < v<sup>′</sup> , (18) does not hold. In conclusion, we obtain that a mechanism could not be truthful if xi(v) > xi(v<sup>′</sup> ), and hence, the allocation function xi(v) must be monotonously non-decreasing. 

Auction Design for Bidders with Ex Post ROI Constraints 

21 

## C Proof of Uniqueness of Payment (Step 3 of Theorem 2) 

Lemma 8 (Uniquessness of Payment). Given any monotonically non-decreasing allocation rule x(·) and p(0) = 0, there exists a unique payment rule p(·) such that (x, p) is DSIC. 

Proof. For any bidder i and any vi ∈ [0, vmax]. We consider two valuations vi and wi = vi + δ for some sufficiently small δ > 0. Following the payment sandwich inequality techniques used in the original Myerson’s proof, we have 

u(vi, vi) ≥ u(wi, vi) and u(wi, wi) ≥ u(wi, vi). 

This gives us two inequalities that can together sandwich the payment pi(v). If we follow Myerson’s original analysis and replace each utility with the value minus the payment for the bidder, these two inequalities would give us 

Mivi(xi(wi) − xi(vi)) ≤ pi(wi) − pi(vi) ≤ Miwi(xi(wi) − xi(vi)). 

In the limit, as δ approaches 0, we can divide each side by δ and get 


![](assets/wine23/wine23.pdf-0021-09.png)


The uniqueness of the payment rule then follows by integrating (19) from 0 to each value v. However, this argument has a problem in the ROI-constrained setting: because of the extra factor Mi in the payment function due to the ROI condition, it is possible that at some point the payment grows to be larger than the bidder’s obtained value, therefore violating the IR condition. 

To deal with this issue, we first note that p(vi) ≤ vi · xi(vi) ≤ wi · xi(vi). This means when bidder i has value wi and misreports her value as vi, her payment will never violate the IR condition. This means we only need to discuss the case when the bidder i with value vi misreports to wi. There are two cases to discuss. 

- If there exists a neighborhood of vi, such that by applying (19) to pi(vi) to get pi(wi), we have pi(wi) ≤ vi · xi(wi). This means in this small neighborhood, the other direction of misreporting will also not be affected by the IR condition. Myerson’s analysis can go through, and the derivative of pi(·) remains fixed and unique at point vi. 

- If for any small neighborhood of vi, applying (19) gives pi(wi) > vi · xi(wi). This means bidder i with value vi would not want to misreport her bid as wi because it would violate the IR condition for her. Here we notice vixi(wi) < pi(wi) ≤ wixi(wi) must hold. When δ is sufficiently small, it implies that we must have pi(wi) = wixi(wi). This suggests that even though we can no longer apply equation (19) in this case. pi(wi) is still a unique and fixed value. 

Combining the two cases together, we know that at each point v ∈ [0, vmax], pi(v) is always unique, therefore proving this claim. 

22 H. Lv et al. 

## D Proof of Lemma 3 

Proof. We prove this statement by contradiction. Suppose the claim is not true at valuation v<sup>∗</sup> , then we have v<sup>∗</sup> = arg max0≤z≤v∗ {M �p(z) − zx(z)} (if there are multiple such v<sup>∗</sup> , choose the smallest one). This means for all 0 ≤ v < v<sup>∗</sup> , the difference d(v, v<sup>∗</sup> ) between M �p(v<sup>∗</sup> ) − v<sup>∗</sup> x(v<sup>∗</sup> ) and M �p(v) − vx(v) is positive: 


![](assets/wine23/wine23.pdf-0022-03.png)


Given allocation x(·), our plan is to construct a new monotone allocation rule, which together with the corresponding payment rule can generate a higher revenue. More specifically, we select a sufficiently small δ > 0 such that letting d(v, v<sup>∗</sup> ) = 0 by increasing the allocation x(v) in the interval (v<sup>∗</sup> − δ, v<sup>∗</sup> ) does not break the monotonicity of the allocation rule. Then, the new allocation rule x¯(·) is defined as 


![](assets/wine23/wine23.pdf-0022-05.png)


This way, for all values v ∈ (v<sup>∗</sup> − δ, v<sup>∗</sup> ), with respect to x¯(·), we have 


![](assets/wine23/wine23.pdf-0022-07.png)



![](assets/wine23/wine23.pdf-0022-08.png)


Then, we prove that x¯(v) > x(v) for all values v ∈ (v<sup>∗</sup> − δ, v). Assume by contradiction that for any δ > 0, there exists some v ∈ (v<sup>∗</sup> −δ, v<sup>∗</sup> ) such that ¯x(v) ≤ x(v). Because we have assumed that both x¯(·) and x(·) are right-differentiable and only have finite non-differentiable points, this means there must exist some δ<sup>′</sup> > 0, 

Auction Design for Bidders with Ex Post ROI Constraints 23 

such that x¯(v) ≤ x(v) holds for all v ∈ (v<sup>∗</sup> − δ<sup>′</sup> , v<sup>∗</sup> ). Pick an arbitrary v in this interval. We then have 


![](assets/wine23/wine23.pdf-0023-02.png)


where the first equality is by Equation (20) and the last equality is by Equation (21). This is a direct contradiction to our previous claim that d(v, v<sup>∗</sup> ) > 0 for all v < v<sup>∗</sup> . Therefore, we obtain that x¯(·) remains non-decreasing because we only modify x in the interval of (v<sup>∗</sup> − δ, v<sup>∗</sup> ) and we have: (1) x¯(v) > x(v) for all values v ∈ (v<sup>∗</sup> − δ, v<sup>∗</sup> ); (2) x¯(v) is increasing in (v<sup>∗</sup> − δ, v<sup>∗</sup> ); and (3) x¯(v) is continuous at v<sup>∗</sup> . 

Finally, we analyze the revenue generated by x¯(·). Let q(·) be the corresponding payment rule of x¯(·) derived from Theorem 2. We compare q(v) and p(v) at each value v. 

- When v ≤ v<sup>∗</sup> −δ, we have q(v) = p(v). This is because the allocation remains unchanged in the interval [0, v<sup>∗</sup> − δ), and the payment of a bid at value v only depends on the allocation at interval [0, v]. 

- When v ∈ (v<sup>∗</sup> − δ, v<sup>∗</sup> ), we always have v ∈ arg max0≤z≤v{M �p(z) − zx¯(z)}, which means the payment of q(v) reduces to the first price, and we have q(v) = vx¯(v) > vx(v) ≥ p(v). 

- When v ≥ v<sup>∗</sup> , we again have q(v) = p(v). This is because when v ≥ v<sup>∗</sup> , we have v<sup>∗</sup> ∈ arg max0≤z≤v{M �p(z) − zx(z)} for both (x, p) and (¯x, q). Then the payment formulation of (4) reduces to 

p(v) = M �p(v) − (M �p(v<sup>∗</sup> ) − v<sup>∗</sup> x(v<sup>∗</sup> )) = v<sup>∗</sup> x(v<sup>∗</sup> ) + M (p�(v) − p�(v<sup>∗</sup> )). 

This payment only depends on the allocation at interval [v<sup>∗</sup> , v], which again x(·) and x¯(·) agree on. 

Combining these cases together, we have<sup>�</sup> v<sup>q(v)f(v) dv>�</sup> v<sup>p(v)f(v) dv.That</sup> is, the new mechanism (¯x, q) has a higher revenue compared to (x, p). This is a contradiction, and this completes the proof. 

## E Proof of Lemma 4 

Proof. Assume that in some revenue-maximizing auction (x, p), there exists a value v such that the two conditions claimed in the lemma do not hold. That is, we have p(v) < vx(v), and x<sup>′</sup> (v) > 0 or x<sup>′</sup> (v) does not exist. Since x(·) is right-differentiable with finite non-differentiable points, by Theorem 2, we have 

24 H. Lv et al. 

p(·) is also continuous at all but a finite number of points in its domains. This means we can always find an interval [v, ¯v], such that p(v) < vx(v) and x<sup>′</sup> i<sup>(v) > 0</sup> for all valuations v ∈ [v, ¯v]. 

Recall that when p(v) < vx(v) for all v, by Lemma 3, the payment reduces to p(v) = M �p(v) and we can write the revenue of the mechanism as rev = M<sup>�</sup> 0<sup>vmax</sup> φ(z)x(z)f (z) dz. Next, we look at the virtual values φ(v) within this interval [v, ¯v]. Our plan is to modify the allocation x(v) in (a subinterval of) this interval based on the sign of φ(v) while maintaining the monotonicity of x(·) and p(v) < vx(v) in the interval, and the expected revenue will (weakly) increase. We consider the following three cases: 

- There exists an interval [a, b] ⊆ [v, ¯v] such that φ(v) > 0, ∀v ∈ [a, b]. In this case, we define 


![](assets/wine23/wine23.pdf-0024-04.png)


where δ > 0 is sufficiently small such that: 1. x¯(·) is still non-decreasing; and 

2. p(v) < vx¯(v) still holds in the interval [v, ¯v], which means the corresponding payment is still p(v) = M �p(v) in this interval. Conditions (1) and (2) imply we can still write the expected revenue as 


![](assets/wine23/wine23.pdf-0024-07.png)


for the new mechanism with allocation x¯. In the meanwhile, x¯(v) is pointwise larger than x(v) at all values v ∈ [a, b] where φ(v) is always positive, and outside this interval the two allocations remain the same. This means x¯(·), together with its corresponding payment rule, would yield strictly higher revenue than the previous mechanism. A contradiction. 

– There exists an interval [a, b] in [v, ¯v] such that φ(v) < 0, ∀v ∈ [a, b]. Similar to the first case, we define 


![](assets/wine23/wine23.pdf-0024-10.png)


where δ > 0 is sufficiently small such that x¯(·) is still non-decreasing and p(v) < vx(v) still holds in the interval [v, ¯v]. Using the same argument as in the previous case, we can again argue that x¯(·) gives a higher revenue than x(·). Again a contradiction. 

- If neither of the first two cases happens, we must have φ(v) = 0, ∀v ∈ [v, ¯v]. In this case, as long as the monotonicity of x(·) and p(v) ≤ vx(v) is maintained in the interval, any modification of x(·) would generate the same revenue. Therefore we can always find an allocation x¯(·) that satisfies one of the required two conditions and have the same revenue as that of x(·). Therefore x¯(·) still gives a revenue-maximizing auction. 

This concludes the proof. 

