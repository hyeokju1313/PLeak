# PLeak

##### mkdir results

## Extended Edit Distance
  ---                                                                                                                   
  Extended Edit Distance                                                                                
                                                                                                                        
  $$\text{EED} = \min\left(1,\ \frac{d(H, R) + \rho \cdot \text{cov}}{|R| + \rho \cdot \text{cov}}\right)$$             
                                                                                                                        
  동적 프로그래밍으로 각 셀 비용을 계산:                                                                                
                                                                                                                        
  $$d_{i,j} = \min \begin{cases}                                                                                        
  d_{i-1,\ j} + \delta_{\text{del}} & \text{(deletion)} \\                                                              
  d_{i-1,\ j-1} + \mathbb{1}[h_i \neq r_j] & \text{(substitution / match)} \\                                           
  d_{i,\ j-1} + \delta_{\text{ins}} & \text{(insertion)} \\                                                             
  \alpha + d_{k,\ j} & \text{(jump from position } k\text{)}                                                            
  \end{cases}$$                                                                                                         
                                                                                                                        
  Coverage 패널티:                                                                                                      
                  
  $$\text{cov} = \sum_{j} \max(0,\ \text{visits}(j) - 1)$$                                                              
                                                                                                                        
  ---                                                                                                                   
  렌더링하면:     
             
  $$\text{EED} = \min\left(1,\ \frac{d(H, R) + \rho \cdot \text{cov}}{|R| + \rho \cdot \text{cov}}\right)$$
                                                                                                                        
  $$d_{i,j} = \min \begin{cases} d_{i-1,\ j} + \delta_{\text{del}} & \text{(deletion)} \ d_{i-1,\ j-1} + \mathbb{1}[h_i 
  \neq r_j] & \text{(substitution / match)} \ d_{i,\ j-1} + \delta_{\text{ins}} & \text{(insertion)} \ \alpha + d_{k,\  
  j} & \text{(jump from position } k\text{)} \end{cases}$$                                                              
                  
  ---
  파라미터 설명
⏺ | 기호 | 기본값 | 의미 |                                                                                              
  |------|--------|------|                                                                                              
  | $H$ | - | 예측 문장 (Hypothesis) |
  | $R$ | - | 정답 문장 (Reference) |                                                                                   
  | $\delta_{\text{del}}$ | 0.2 | 삭제 비용 |                                                                           
  | $\delta_{\text{ins}}$ | 1.0 | 삽입/치환 비용 |                                                                      
  | $\alpha$ | 2.0 | Jump 패널티 |                                                                                      
  | $\rho$ | 0.3 | Coverage 패널티 계수 |

## Semantic Similarity
$$\text{Semantic Similarity} = \cos(\theta) = \frac{\vec{e_1} \cdot \vec{e_2}}{|\vec{e_1}| \cdot |\vec{e_2}|}$$
