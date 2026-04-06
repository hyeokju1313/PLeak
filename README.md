# PLeak

##### mkdir results

## Extended Edit Distance
$$\text{EED} = \min\left(1,\ \frac{d(H, R) + \rho \cdot \text{cov}}{|R| + \rho \cdot \text{cov}}\right)$$

#### 동적 프로그래밍으로 각 셀 비용을 계산
$$d_{i,j} = \min \begin{cases}                                                                                        
  d_{i-1,\ j} + \delta_{\text{del}} & \text{(deletion)} \\                                                              
  d_{i-1,\ j-1} + \mathbb{1}[h_i \neq r_j] & \text{(substitution / match)} \\                                           
  d_{i,\ j-1} + \delta_{\text{ins}} & \text{(insertion)} \\                                                             
  \alpha + d_{k,\ j} & \text{(jump from position } k\text{)}                                                            
  \end{cases}$$

#### Coverage 패널티
$$\text{cov} = \sum_{j} \max(0,\ \text{visits}(j) - 1)$$

#### 렌더링하면 
$$\text{EED} = \min\left(1,\ \frac{d(H, R) + \rho \cdot \text{cov}}{|R| + \rho \cdot \text{cov}}\right)$$
                                                                                                                        
$$d_{i,j} = \min \begin{cases} d_{i-1,\ j} + \delta_{\text{del}} & \text{(deletion)} \ d_{i-1,\ j-1} + \mathbb{1}[h_i 
  \neq r_j] & \text{(substitution / match)} \ d_{i,\ j-1} + \delta_{\text{ins}} & \text{(insertion)} \ \alpha + d_{k,\  
  j} & \text{(jump from position } k\text{)} \end{cases}$$

## Semantic Similarity
$$\text{Semantic Similarity} = \cos(\theta) = \frac{\vec{e_1} \cdot \vec{e_2}}{|\vec{e_1}| \cdot |\vec{e_2}|}$$
