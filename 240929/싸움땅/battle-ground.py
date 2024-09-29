arr=[]
N,M,K= map(int,input().split())
for i in range(N): # 총 맵
    arr.append(list(map(int,input().split())))
for i in range(N): # 총 맵 set으로 설정
    for j in range(N):
        a=set()
        a.add(arr[i][j])
        arr[i][j]=a

board=[[0]*N for _ in range(N)] # 플레이어 맵
plyer=[0]*(M+1) # x,y,d,s
for i in range(1,M+1):
    plyer[i]=list(map(int,input().split()))
    x,y=plyer[i][0]-1,plyer[i][1]-1
    board[x][y]=i
    plyer[i][0], plyer[i][1] =x,y

# N,M,K=5,4,6
# # plyer=[0]*(M+1) # x,y,d,s
# plyer=[[[] for _ in range(4)] for _ in range(M+1)]
# board=[[0]*N for _ in range(N)] # 플레이어 맵
# arr=[[1,2,0,1,2],[1,0,3,3,1],[1,3,0,2,3],[2,1,2,4,5],[0,1,3,2,0]]
# for i in range(N): # 총 맵 set으로 설정
#     for j in range(N):
#         a=set()
#         a.add(arr[i][j])
#         if arr[i][j]==0:
#             a.remove(arr[i][j])
#         arr[i][j]=a
# 
# plyer[1]=[0,2,2,3]
# plyer[2]=[1,1,1,5]
# plyer[3]=[2,2,2,2]
# plyer[4]=[4,0,3,4]
# for i in range(1,M+1):
#     x,y=plyer[i][0],plyer[i][1]
#     board[x][y]=i

points=[0]*(M+1)
gun=[0]*(M+1)

def get_gun(idx,x,y):
    ## 총 없으면 -> 획득 (gun, arr 모두 수정) 있으면 -> 비교 후 큰 거 획득
    if gun[idx]:
        arr[x][y].add(gun[idx]) # 내 거 먼저 올림
        gun[idx]=0
    if len(arr[x][y])>0:
        g = max(arr[x][y])
        gun[idx] = g
        arr[x][y].remove(g)

def in_range(i,j):
    return 0<=i<N and 0<=j<N

dir = [(-1, 0), (0, 1), (1, 0), (0, -1)]
for k in range(K):
    if k==1:
        ass=1
    for m in range(1,M+1): # 플레이어 순차적으로
        si,sj,sd,pwr = plyer[m][0], plyer[m][1],plyer[m][2],plyer[m][3]
        # [1] 플레이어 이동 -> 격자 나가면 반대 방향으로 한칸
        ni,nj=si+dir[sd][0],sj+dir[sd][1]
        if not in_range(ni,nj):
            ni, nj = si - dir[sd][0], sj - dir[sd][1] #반대 방향으로
            sd=(sd+2)%4
            plyer[m][2]=sd

        plyer[m][0], plyer[m][1]=ni,nj
        board[si][sj] = 0
        # [2] 이동 후
        if board[ni][nj]==0:
        ## 다른 플레이어 없으면 -> 총 확인 후 획득 get_gun(m)
            get_gun(m,ni,nj)
            board[ni][nj]=m
            continue
        else:
            ## 2-1 사람 있으면 -> fight
            pi=board[ni][nj]
            ### 초기+총 비교
            if (plyer[pi][3]+gun[pi]>pwr+gun[m]) or ((plyer[pi][3]+gun[pi]==pwr+gun[m]) and plyer[pi][3]>pwr):
                widx,lidx=pi,m
            else: widx,lidx=m,pi
            reward=abs((plyer[widx][3]+gun[widx])-(plyer[lidx][3]+gun[lidx]))
            points[widx]+=reward
            ## 2-2 lose
            # 총 반납
            li,lj,ld = plyer[lidx][0],plyer[lidx][1],plyer[lidx][2]
            if gun[lidx]:
                arr[li][lj].add(gun[lidx])
            gun[lidx]=0
            # 현재 방향으로 이동 -> 다른 플레이어 있거나 격자 밖 -> 빈칸 보일 때까지 90도 회전 반복 (d+=1,d%4)
            for _ in range(4):
                nni, nnj = ni + dir[ld][0], nj + dir[ld][1]
                if in_range(nni, nnj) and board[nni][nnj]==0:
                    board[nni][nnj] = lidx
                    plyer[lidx][0],plyer[lidx][1] = nni,nnj
                    break
                ld=(ld+1)%4
            plyer[lidx][2]=ld ##
            ## 총 획득 get_gun(lose_idx)
            if len(arr[nni][nnj])>0 :
                get_gun(lidx,nni,nnj)
            ## 2-3 win
            get_gun(widx,ni,nj)
            board[ni][nj] = widx
            plyer[widx][0], plyer[widx][1] = ni,nj


for p in points[1:]:
    print(p,end=" ")