# PLeak

##### mkdir results

## Extended Edit Distance
  ---                                                                                                                   
  Extended Edit Distance                                                                                
                                                                                                                        
  $$\text{EED} = \min\left(1,\ \frac{d(H, R) + \rho \cdot \text{cov}}{|R| + \rho \cdot \text{cov}}\right)$$             
                                                                                                                        
  동적 프로그래밍으로 각 셀 비용을 계산                                                                                
                                                                                                                        
  $$d_{i,j} = \min \begin{cases}                                                                                        
  d_{i-1,\ j} + \delta_{\text{del}} & \text{(deletion)} \\                                                              
  d_{i-1,\ j-1} + \mathbb{1}[h_i \neq r_j] & \text{(substitution / match)} \\                                           
  d_{i,\ j-1} + \delta_{\text{ins}} & \text{(insertion)} \\                                                             
  \alpha + d_{k,\ j} & \text{(jump from position } k\text{)}                                                            
  \end{cases}$$                                                                                                         
                                                                                                                        
  Coverage 패널티                                                                                                      
                  
  $$\text{cov} = \sum_{j} \max(0,\ \text{visits}(j) - 1)$$                                                              
                                                                                                                        
  ---                                                                                                                   
  렌더링     
             
  $$\text{EED} = \min\left(1,\ \frac{d(H, R) + \rho \cdot \text{cov}}{|R| + \rho \cdot \text{cov}}\right)$$
                                                                                                                        
  $$d_{i,j} = \min \begin{cases} d_{i-1,\ j} + \delta_{\text{del}} & \text{(deletion)} \ d_{i-1,\ j-1} + \mathbb{1}[h_i 
  \neq r_j] & \text{(substitution / match)} \ d_{i,\ j-1} + \delta_{\text{ins}} & \text{(insertion)} \ \alpha + d_{k,\  
  j} & \text{(jump from position } k\text{)} \end{cases}$$                                                              
                  
  ---
  파라미터 설명
  
  | 기호 | 기본값 | 의미 |                                                                                              
  |------|--------|------|                                                                                              
  | $H$ | - | 예측 문장 (Hypothesis) |
  | $R$ | - | 정답 문장 (Reference) |                                                                                   
  | $\delta_{\text{del}}$ | 0.2 | 삭제 비용 |                                                                           
  | $\delta_{\text{ins}}$ | 1.0 | 삽입/치환 비용 |                                                                      
  | $\alpha$ | 2.0 | Jump 패널티 |                                                                                      
  | $\rho$ | 0.3 | Coverage 패널티 계수 |

## Semantic Similarity
  ---                                                                        
  PLeak Semantic Similarity 평가 방식                                                                                   
                                                                                                                        
  전체 흐름                                                                                                             
                                                                                                                        
  입력 문장 (예측 / 정답)
          ↓                                                                                                             
    SentenceTransformer 인코딩
    (all-MiniLM-L6-v2)                                                                                                  
          ↓                                                                                                             
    임베딩 벡터 생성
          ↓                                                                                                             
    코사인 유사도 계산
          ↓                                                                                                             
    평균 / 표준편차 출력
                                                                                                                        
  ---             
  Step 1 — 입력 데이터 구성
                                                                                                                        
  results는 {context(정답), trigger(예측)} 형태의 딕셔너리 리스트입니다.
                                                                                                                        
  keys = list(results[0].keys())
  keys[0] = "context"  → 정답 문장 (target)                                                                           
  keys[1] = trigger    → 모델이 생성한 예측 문장 (prediction)                                                         
                                                                                                                        
  ---                                                                                                                   
  Step 2 — 문장 임베딩                                                                                                  
                      
  전처리 없이 원문 그대로 all-MiniLM-L6-v2 모델에 입력합니다.
                                                                                                                        
  $$\vec{e_1} = \text{Encode}(H), \quad \vec{e_2} = \text{Encode}(R)$$                                                  
                                                                                                                        
  - $H$: 예측 문장 (Hypothesis)                                                                                         
  - $R$: 정답 문장 (Reference)
  - $\text{Encode}(\cdot)$: 384차원 밀집 벡터로 변환                                                                    
                                                                                                                        
  ▎ Exact Match / Substring과 달리 알파벳 필터링(filter_tokens) 없이 원문 그대로 사용합니다.                            
                                                                                                                        
  ---                                                                                                                   
  Step 3 — 코사인 유사도 계산
                                                                                                                        
  $$\text{sim}(H, R) = \cos(\theta) = \frac{\vec{e_1} \cdot \vec{e_2}}{|\vec{e_1}| \cdot |\vec{e_2}|}$$
    | 값 | 의미 |                                                                                                         
  |----|------|   
  | $1.0$ | 두 문장의 의미가 완전히 동일 |
  | $0.0$ | 두 문장의 의미가 무관 |                                                                                     
  | $-1.0$ | 두 문장의 의미가 정반대 |

  ---                                                                                                                   
  Step 4 — 전체 샘플 집계
                         
  $$\mu = \frac{1}{N}\sum_{i=1}^{N} \text{sim}(H_i, R_i), \quad \sigma = \sqrt{\frac{1}{N}\sum_{i=1}^{N}(\text{sim}(H_i,
   R_i) - \mu)^2}$$                                                                                                     
   
  - $N$: 전체 샘플 수                                                                                                   
  - 결과를 CatMetric에 누적 후 torch.std_mean()으로 평균($\mu$)과 표준편차($\sigma$)를 함께 출력
                                                                                                                        
  ---
  다른 메트릭과의 비교
  | 메트릭 | 전처리 | 측정 대상 |
  |--------|--------|-----------|                                                                                       
  | Exact Match | 알파벳만 추출, 소문자 | 문자열 완전 일치 |
  | Substring | 알파벳만 추출, 소문자 | 부분 문자열 포함 여부 |                                                         
  | EED | 없음 (원문) | 문자 단위 편집 거리 |                                                                           
  | **Semantic Similarity** | **없음 (원문)** | **의미적 유사도 (벡터 공간)** |
