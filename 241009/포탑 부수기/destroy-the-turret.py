N,M,K=map(int,input().split())
arr=[list(map(int,input().split())) for _ in range(N)]

for i in range(N):
    for j in range(M):
        power=arr[i][j]
        arr[i][j]=[power,0] # 공격력과 최근 공격 TURN
p=0
def pprint(arr):
    if p: print("공격력")
    if p: print("\n".join(' '.join( f"{elem[0]:>4}" for elem in l) for l in arr))
    if p: print("최근 공격 턴")
    if p: print("\n".join(' '.join(f"{elem[1]:>4}" for elem in l) for l in arr))

def weak():
    mn = 5001
    mlst=[]
    for i in range(N):
        for j in range(M):
            if arr[i][j][0] == 0:
                continue
            if mn > arr[i][j][0]:
                mn = arr[i][j][0]
                mlst = [[i, j, arr[i][j][0], arr[i][j][1]]] # 좌표, [공격력, 최근 공격 턴]
            elif mn == arr[i][j][0]:
                mlst.append([i, j, arr[i][j][0], arr[i][j][1]])  # 좌표 i(행)[0], 열[1], 공격력[2], 최근 공격 턴[3]

    mlst.sort(key=lambda x: (-x[3], -(x[0] + x[1]), -x[1]))
    weakest = mlst[0]  # 좌표, 공격력, 최근 공격 턴

    # weakest[2] += (N + M)  # N+M만큼 공격력 상승
    # weakest[3] = turn  # 현재 턴이 최근 공격 turn # 여기에 40분
    return weakest

def strong():
    mx = 0
    tlst = []
    for i in range(N):
        for j in range(M):
            if arr[i][j][0] <= 0:
                continue
            if mx < arr[i][j][0]:  # 현재 공격력이 더 작으면
                mx = arr[i][j][0]
                tlst = [[i, j, arr[i][j][0], arr[i][j][1]]] # 좌표, [공격력, 최근 공격 턴]
            elif mx == arr[i][j][0]:
                tlst.append([i, j, arr[i][j][0], arr[i][j][1]])  # 좌표 i(행)[0], 열[1], 공격력[2], 최근 공격 턴[3]

    tlst.sort(key=lambda x: (x[3], (x[0] + x[1]), x[1]))  # -> 소팅은 키가 필요
    strongest = tlst[0]  # 좌표, 공격력, 최근 공격 턴
    return strongest



from collections import deque
def bfs(si,sj,ei,ej): # 레이저 공격 경로 반환 (ei,ej)까지 최단 경로 반환/ 없으면-> False 반환 //  건너편도 가능(%N,%M)
    v=[[0]*M for _ in range(N)]
    v[si][sj]=(si,sj)
    q=deque([(si,sj)])
    while q:
        ci,cj=q.popleft()
        if (ci, cj) == (ei, ej):  # 목적지 좌표 도달
           while True:
                ci,cj = v[ci][cj]  # 그 전 좌표
                if (ci,cj) == (si, sj):  # 처음 좌표면
                    return True
                fset.add((ci,cj))
        for di,dj in ((0,1),(1,0),(0,-1),(-1,0)): # 우하좌상 네 방향
            ni,nj=(ci+di)%N,(cj+dj)%M # 건너편까지 가능
            # 미방문 ---> ei,ej 도달하면 역추적, 조건: 0이 아님
            if v[ni][nj]==0 and arr[ni][nj][0]>0:
                q.append((ni,nj))
                v[ni][nj]=(ci,cj) # 오기 바로 전 좌표
    return False
import copy
#+==============================================================
for turn in range(1,K+1): # arr[][][0] : 공격력 / arr[][][1] : 최근 공격 turn
    if p: print(f"============{turn}턴 시작=================")
    if p: pprint(arr)
    # [1] 공격자 선정
    weakest=weak()
    # [2] 공격 대상 선정
    strongest=strong()
    if p: print("============공격자/ 공격 대상 선정 완료=================")
    if p: pprint(arr)

    if p: print("공격자",weakest)
    if p: print("공격 대상", strongest)

    weakest[2]+=(N+M)
    # 공격!
    si,sj,d,s_turn=weakest
    ei,ej,_,e_turn=strongest
    arr[si][sj] = [weakest[2], turn] # 나중에 업데이트해야 강한 애가 안 되지
    fset=set()
    if p: print("============공격자 업데이트=================")
    if p: pprint(arr)

    if bfs(si,sj,ei,ej): # [2-1] 레이저 공격
        for pi,pj in fset:
            if arr[pi][pj][0]>0: # 0이 아니면
                arr[pi][pj][0]-= (d//2)
        if p: print("============레이저 공격=================")
        if p: pprint(arr)
        if p: print(f"가는 경로",fset)

    elif bfs(si,sj,ei,ej)==False: #[2-2] 포탄 공격
        for di,dj in ((0,1),(1,0),(0,-1),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)):
            ni,nj=(ei+di)%N,(ej+dj)%M # 포탄 기준 8방향
            if (ni,nj)!=(si,sj):
                if arr[ni][nj][0]>0: # 살아 있으면
                    fset.add((ni,nj))
                    arr[ni][nj][0]-=(d//2) # 8방향에 있는 애들
        if p: print("============포탄 공격=================")
        if p: pprint(arr)
        if p: print(f"주변 경로", fset)

    # 공격 대상
    arr[ei][ej][0] -= d
    if p: print("============마지막 좌표 공격=================")
    if p: pprint(arr)

    # [3] 포탑 부서짐
    cnt = N * M
    for i in range(N):
        for j in range(M):
            if arr[i][j][0]<=0:
                arr[i][j][0]=0 # 최솟값은 0으로
                cnt-=1
    if p: print("============포탑 부서짐================")
    if p: pprint(arr)

    fset.add((ei,ej))
    fset.add((si,sj))

    # [4] 포탑 정비
    for i in range(N):
        for j in range(M):
            if arr[i][j][0]>0 and (i,j) not in fset: # 안 부서졌고, 공격에 참여 안 했으면
                arr[i][j][0]+=1
    if p: print("============포탑 정비 완료================")
    if p: pprint(arr)

    if cnt<=1:
        break
    if p: print(f"산 놈들 {cnt}명")

last_strong=strong()
print(last_strong[2])