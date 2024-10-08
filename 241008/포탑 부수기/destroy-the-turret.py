N,M,K=map(int,input().split())
arr=[list(map(int,input().split())) for _ in range(N)]

for i in range(N):
    for j in range(M):
        power=arr[i][j]
        arr[i][j]=[power,0] # 공격력과 최근 공격 TURN

def weak(turn):
    mn = 1001
    flag = 0
    for i in range(N):
        for j in range(M):
            if arr[i][j][0] == 0:
                continue
            if mn > arr[i][j][0]:
                mn = arr[i][j][0]
                mlst = [i, j, arr[i][j][0], arr[i][j][1]]  # 좌표, [공격력, 최근 공격 턴]
                flag = 0
            elif mn == arr[i][j][0]:
                mlst.append([i, j, arr[i][j][0], arr[i][j][1]])  # 좌표 i(행)[0], 열[1], 공격력[2], 최근 공격 턴[3]
                flag = 1
    if flag:  # 다차원 배열
        mlst.sort(key=lambda x: (-x[2], -(x[0] + x[1]), -x[1]))
        weakest = mlst[0]  # 좌표, 공격력, 최근 공격 턴
    else:
        weakest = mlst
    weakest[2] += (N + M)  # N+M만큼 공격력 상승
    weakest[3] = turn  # 현재 턴이 최근 공격 turn # 여기에 40분
    return weakest

def strong():
    mx = 0
    tlst = []
    for i in range(N):
        for j in range(M):
            if arr[i][j][0] == 0:
                continue
            if mx < arr[i][j][0]:  # 현재 공격력이 더 작으면
                mx = arr[i][j][0]
                tlst = [i, j, arr[i][j][0], arr[i][j][1]]  # 좌표, [공격력, 최근 공격 턴]
                flag = 0
            elif mx == mx == arr[i][j][0]:
                tlst.append([i, j, arr[i][j][0], arr[i][j][1]])  # 좌표 i(행)[0], 열[1], 공격력[2], 최근 공격 턴[3]
                flag = 1
    if flag:  # 다차원 배열
        tlst.sort(key=lambda x: (x[2], (x[0] + x[1]), x[1])) #-> 소팅은 키가 필요
        strongest = tlst[0]  # 좌표, 공격력, 최근 공격 턴
    else:
        strongest = tlst
    return strongest

from collections import deque
def bfs(si,sj,ei,ej): # 레이저 공격 경로 반환 (ei,ej)까지 최단 경로 반환/ 없으면-> False 반환 //  건너편도 가능(%N,%M)
    v=[[0]*M for _ in range(N)]
    v[si][sj]=(si,sj)
    q=deque([(si,sj)])
    path=[]
    while q:
        ci,cj=q.popleft()
        for di,dj in ((0,1),(1,0),(0,-1),(-1,0)): # 우하좌상 네 방향
            ni,nj=(ci+di)%N,(cj+dj)%M # 건너편까지 가능
            # 미방문 ---> ei,ej 도달하면 역추적
            if v[ni][nj]==0:
                q.append((ni,nj))
                v[ni][nj]=(ci,cj) # 오기 바로 전 좌표
                if (ni, nj) == (ei, ej):  # 대상에 도착 -> 역추적 시작
                    while True:
                        ni, nj = v[ni][nj]  # 그 전 좌표
                        if (ni, nj) == (si, sj):  # 처음 좌표면
                            return path[::-1]
                        path.append((ni, nj))
    return False

for turn in range(1,K+1): # arr[][][0] : 공격력 / arr[][][1] : 최근 공격 turn
    # [1] 공격자 선정
    weakest=weak(turn)
    # [2] 공격 대상 선정
    strongest=strong()

    # 공격!
    si,sj,spwr,s_turn=weakest
    ei,ej,epwr,e_turn=strongest
    path=bfs(si,sj,ei,ej) # 시작이랑 끝은 포함 X    # 튜플 좌표가 원소인 배열

    if path: # [2-1] 레이저 공격
        for pi,pj in path:
            if arr[pi][pj][0]>0: # 0이 아니면
                arr[pi][pj][0]-= (spwr//2)

    else: #[2-2] 포탄 공격
        path = []
        for di,dj in ((0,1),(1,0),(0,-1),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)):
            ni,nj=(ei+di)%N,(ej+dj)%M # 포탄 기준 8방향
            if arr[ni][nj]>0: # 살아 있으면
                path.append((ni,nj))
                arr[ni][nj][0]-=(spwr//2) # 8방향에 있는 애들
    # 공격 대상
    arr[ei][ej][0] -= spwr

    # [3] 포탑 부서짐
    cnt = N * M
    for i in range(N):
        for j in range(M):
            if arr[i][j][0]<0:
                arr[i][j][0]=0 # 최솟값은 0으로
                cnt-=1

    path+=[(ei,ej),(si,sj)]

    # [4] 포탑 정비
    for i in range(N):
        for j in range(M):
            if arr[i][j][0]>0 and (i,j) not in path: # 안 부서졌고, 공격에 참여 안 했으면
                arr[i][j][0]+=1 # 최솟값은 0으로

    if cnt==1:
        break

last_strong=strong()
print(last_strong[2])