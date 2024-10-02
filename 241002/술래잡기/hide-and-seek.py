N,M,H,K = map(int,input().split())
## 술래 direction list 생성 ->> 이상
dir = {1:(0,1),2:(1,0),3:(0,-1),4:(-1,0)}
d=[]
for i in range(1,N+1):
    if (i % 2) == 1: # 홀
        for _ in range(i):
            d.append(4)
        if i == N: break
        for _ in range(i):
            d.append(1)
    else: # 짝
        for _ in range(i):
            d.append(2)
        for _ in range(i):
            d.append(3)

d=(d+d[::-1])*(K//(2*N**2)+1)
d=d[:K+1]
######################
runners=[]
trees=[]
arr=[[0]*N for _ in range(N)]
for _ in range(M):
    i,j,rd=map(int,input().split())
    runners.append([[i-1,j-1],rd])
    arr[i-1][j-1]+=1

for _ in range(H):
    i, j = map(int, input().split())
    trees.append((i-1,j-1))
# 술래 정의 (좌표, 방향)
chaser = (N//2,N//2) # direction은 라운드마다 따로
arr[N//2][N//2]=-1 # 술래: -1

def cal_dist(i,j):
    global chaser
    ci,cj=chaser[0],chaser[1]
    return abs(ci-i)+abs(cj-j)

def in_range(i,j):
    return 0<=i<N and 0<=j<N

dir = {1:(0,1),2:(1,0),3:(0,-1),4:(-1,0)}
op={1:3,2:4,3:1,4:2}
out=[False]*M
score=0

## 게임 시작
for k in range(1,K+1):
    if len(out)==0:
        break
    # [1] 도망자 이동
    # 거리 3이하인 애들만 가능
    for i,run in enumerate(runners):
        ri, rj = run[0]
        rd = run[1]
        if out[i] or cal_dist(ri,rj)>3:
            continue
        # 도망 시작
        ni,nj=ri+dir[rd][0],rj+dir[rd][1]
        if in_range(ni,nj):
            if arr[ni][nj]==-1: # 술래 있으면
                continue
            else: # 없으면
                arr[ni][nj] += 1
                arr[ri][rj] -= 1
        else: # 범위 밖
            rd=op[rd]
            runners[i][1] = rd # update
            ni, nj = ri + dir[rd][0], rj + dir[rd][1]
            if arr[ni][nj]==-1:
                continue
            else:
                arr[ni][nj] += 1
                arr[ri][rj] -= 1
        runners[i][0] = (ni, nj)
        # out range and arr[ni][nj]!=-1 면 방향 바꿔 한칸 rd=op[rd]
        # in range-> arr[ni][nj]!=-1면(술래 없으면) 한 칸/ 술래 있으면 continue
        ## 좌표,방향 업데이트 -> arr 에 반영 arr[ni][nj]-=1 ,runners[i][0]=(ni,nj),runners[i][1]=rd

    ## [2] 술래 이동
    # 술래 방향 업데이트
    out_cnt=0
    ci,cj=chaser # 현재 위치
    ### 달팽이 모양
    if (ni,nj)==(N//2,N//2): # 시작과 끝부분은 바로 방향 변경
        dd=4
    elif (ni,nj)==(0,0):
        dd=2
    else:
        dd =d[k - 1] # 현재 바라보는 방향
    cd = dir[dd] # 다음 좌표로 움직이기 위한 방향
    ni, nj = ci + cd[0], cj + cd[1]   # 한 칸씩 이동
    arr[ci][cj]=0
    arr[ni][nj]=-1
    cd=dir[d[k]]
    # 시야 내 탐색
    for i in range(3):
        ti, tj = ni + cd[0]*(i+1), nj + cd[1]*(i+1)  # 한 칸씩 이동
        if in_range(ti,tj) and arr[ti][tj]>0: # 도망자 한 명 이상 있으면
            if (ti,tj) in trees:
                continue
            else:
                out_cnt+=arr[ti][tj]
                for idx,run in enumerate(runners):
                    if run[0]==(ti,tj):
                        out[idx]=True
                arr[ti][tj]=0
        # 3칸 내 있으면 -> 나무 확인 -> 없으면 out처리, arr삭제, cnt 증가 -> 있으면 continue
    score+=k*out_cnt
    chaser=(ni,nj)

print(score)