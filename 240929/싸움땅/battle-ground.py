# 입력 처리
N, M, K = map(int, input().split())
arr1 = [list(map(int, input().split())) for _ in range(N)]
arr= [[[] for _ in range(N)] for _ in range(N)]
# arr의 각 요소를 set으로 변환
for i in range(N):
    for j in range(N):
        if arr1[i][j] > 0:
            arr[i][j].append(arr1[i][j])

board = [[0] * N for _ in range(N)]  # 플레이어 맵
plyer = [0] * (M + 1)  # x, y, d, s 초기화

# 플레이어 정보 입력 처리
for i in range(1, M + 1):
    x, y, d, s = map(int, input().split())
    x, y = x - 1, y - 1  # 인덱스 1 감소
    board[x][y] = i  # 플레이어 위치 표시
    plyer[i] = [x, y, d, s]


points=[0]*(M+1)
gun=[0]*(M+1)

def get_gun(idx,x,y): # 비교 후 큰 거는 갖고, 기존에 갖던 건 놓고 가는 로직이 잘 안돼있음
    ## 총 없으면 -> 획득 (gun, arr 모두 수정)
    if len(arr[x][y]) > 0:
        mx=max(arr[x][y])
        if gun[idx]<mx:
            if gun[idx]>0:
                arr[x][y].append(gun[idx])
            arr[x][y].remove(mx)
            gun[idx]=mx

def in_range(i,j):
    return 0<=i<N and 0<=j<N

dir = [(-1, 0), (0, 1), (1, 0), (0, -1)]
# 반대 방향 처리
op={0:2,1:3,2:0,3:1}
for t in range(K):
    for m in range(1,M+1): # 플레이어 순차적으로
        si,sj,sd,pwr = plyer[m][0], plyer[m][1],plyer[m][2],plyer[m][3]
        # [1] 플레이어 이동 -> 격자 나가면 반대 방향으로 한칸
        ni,nj=si+dir[sd][0],sj+dir[sd][1]
        if not in_range(ni,nj):
            ni, nj = si + dir[op[sd]][0], sj + dir[op[sd]][1] #반대 방향으로
            plyer[m][2]=op[sd]
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
            widx, lidx =0,0
            if (plyer[pi][3]+gun[pi]>pwr+gun[m]) or ((plyer[pi][3]+gun[pi]==pwr+gun[m]) and plyer[pi][3]>pwr):
                widx,lidx=pi,m
            else: widx,lidx=m,pi
            reward=abs((plyer[widx][3]+gun[widx])-(plyer[lidx][3]+gun[lidx]))
            points[widx]+=reward
            ## 2-2 lose
            # 총 반납
            li,lj,ld = plyer[lidx][0],plyer[lidx][1],plyer[lidx][2]
            if gun[lidx]:
                arr[li][lj].append(gun[lidx])
                gun[lidx]=0
            # 현재 방향으로 이동 -> 다른 플레이어 있거나 격자 밖 -> 빈칸 보일 때까지 90도 회전 반복 (d+=1,d%4)
            for k in range(4):
                nni, nnj = ni + dir[(ld+k)%4][0], nj + dir[(ld+k)%4][1]
                if in_range(nni, nnj) and board[nni][nnj]==0:
                    if len(arr[nni][nnj]) > 0:
                        get_gun(lidx, nni, nnj)
                    board[nni][nnj] = lidx
                    plyer[lidx][0],plyer[lidx][1] = nni,nnj
                    plyer[lidx][2] = (ld+k)%4  ##
                    break

            ## 총 획득 get_gun(lose_idx)

            ## 2-3 win
            get_gun(widx,ni,nj)
            board[ni][nj] = widx
            plyer[widx][0], plyer[widx][1] = ni,nj


for p in points[1:]:
    print(p,end=" ")