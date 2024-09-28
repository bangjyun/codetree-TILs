from collections import deque

# N, M, K= map(int,input().split())
# arr=[]
# for _ in range(N):
#     arr.append(list(map(int,input().split())))
## TC1
# N,M,K=4,4,1
# arr = [[0,1,4,4],[8,0,10,13],[8,0,11,26],[0,0,0,0]]
#
# ## TC2
N,M,K=4,4,3
arr = [[6,8,0,1],[0,0,0,0],[0,0,0,0],[0,0,8,0]]

attack_turn=[[0]*M for _ in range(N)]

def weakest():
    mn=5000
    mn_pot=[]
    for i in range(N):
        for j in range(M):
            if arr[i][j]<=0:
                continue
            if mn>arr[i][j]:
                mn=arr[i][j]
                mn_pot=[(i,j,attack_turn[i][j])] # 행, 열, 최근 공격 turn
            elif mn==arr[i][j]:
                mn_pot.append((i,j,attack_turn[i][j]))

    mn_pot.sort(key=lambda t:(-t[2],-(t[0]+t[1]),-t[1]))
    # mn_pot.sort(key=lambda x:x[2],reverse=True) # turn이 클수록
    #
    # cur_turn=mn_pot[0][2]
    # msum=[]
    # max_sum=mn_pot[0][0]+mn_pot[0][1]
    # for i,j,turn in mn_pot:
    #     if cur_turn==turn:
    #         if max_sum<=i+j:
    #             msum=[(i,j)]
    #         elif msum==i+j:
    #             msum.append((i, j))
    #
    # msum.sort(key=lambda x:x[1], reverse=True)
    # wi,wj=msum[0]
    wi, wj =mn_pot[0][0],mn_pot[0][1]
    arr[wi][wj]+=(N+M)
    return wi,wj,arr[wi][wj]

def strongest():
    mn = 0
    mn_pot = []
    for i in range(N):
        for j in range(M):
            if arr[i][j]<=0:
                continue
            if mn < arr[i][j]:
                mn = arr[i][j]
                mn_pot = [(i, j, attack_turn[i][j])]  # 행, 열, 최근 공격 turn
            elif mn == arr[i][j]:
                mn_pot.append((i, j, attack_turn[i][j]))

    # mn_pot.sort(key=lambda x: x[2])  # turn이 작을수록
    mn_pot.sort(key=lambda t: (t[2], (t[0] + t[1]), t[1]))
    # cur_turn = mn_pot[0][2]
    # msum = []
    # min_sum = mn_pot[0][0] + mn_pot[0][1]
    # for i, j, turn in mn_pot:
    #     if cur_turn == turn:
    #         if min_sum >= i + j:
    #             msum = [(i, j)]
    #         elif msum == i + j:
    #             msum.append((i, j))
    #
    # msum.sort(key=lambda x: x[1]) # 열이 작을수록
    si,sj= mn_pot[0][0],mn_pot[0][1]

    return si,sj





def bfs(wi, wj, si, sj):
    visited = [[False] * M for _ in range(N)]
    parent = [[None] * M for _ in range(N)]  # 각 노드의 부모 노드를 저장
    visited[wi][wj] = True
    q = deque()
    q.append((wi, wj))

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    # BFS로 탐색 시작
    while q:
        i, j = q.popleft()

        if (i, j) == (si, sj):  # 목표 지점에 도달하면 경로를 역추적
            path = []
            while (i, j) is not None:
                path.append((i, j))  # 현재 좌표를 경로에 추가
                if parent[i][j] is None:
                    break  # 부모가 없으면 종료
                i, j = parent[i][j]  # 부모 노드로 이동
            return path[::-1]  # 경로를 반전시켜 올바른 순서로 반환

        for di, dj in directions:
            ni, nj = i + di, j + dj

            # 경계 처리
            if ni >= N:
                ni = N - ni
            elif ni < 0:
                ni = N+ni

            if nj >= M:
                nj = M - nj
            elif nj < 0:
                nj = M+nj

            # 공격력 0 이하인 곳은 건너뜀
            if arr[ni][nj] <= 0:
                continue

            # 방문하지 않은 노드에 대해 탐색
            if not visited[ni][nj]:
                visited[ni][nj] = True
                parent[ni][nj] = (i, j)  # 부모 노드를 현재 노드로 저장
                q.append((ni, nj))

    return False  # 경로가 없을 경우


#
# def bfs(wi,wj,si,sj):
#     visited = [[False] * M for _ in range(N)]
#     visited[wi][wj]=True
#     q = deque()
#     q.append([wi, wj])
#     trace = deque()
#
#     # 대상까지의 최단 경로
#     while q:
#         v = q.popleft()
#         for di, dj in (0, 1), (1, 0), (0, -1), (-1, 0):
#             ni = v[0] + di
#             nj = v[1] + dj
#             if ni >= N:
#                 ni = N - ni
#             elif ni<0:
#                 ni = N + ni
#
#             if nj >= M:
#                 nj = M - nj
#             elif nj<0:
#                 nj = M + nj
#
#             if arr[ni][nj]<=0:
#                 continue
#
#             if not visited[ni][nj]:
#                 if (ni, nj) == (si, sj):
#                     return trace
#                 if arr[ni][nj] <= 0:  # 공격력 0 이하는 못건넘
#                     continue
#                 visited[ni][nj] = True
#                 q.append([ni, nj])
#                 trace.append([ni, nj])
#     return False

for turn in range(1,K+1):

    attacked = [[False] * M for _ in range(N)]
    # 대상자 선정
    si, sj = strongest()
    # 공격자 선정
    wi,wj,pwr=weakest()

    # 공격
    trace=bfs(wi,wj,si,sj)
    attack_turn[wi][wj] = turn
    attacked[wi][wj]=True

    if trace is not False:
        ## 레이저 공격
        for i,j in trace[1:-1]:
            if arr[i][j] >0:
                arr[i][j] -= pwr // 2
                attacked[i][j] = True

        arr[si][sj]-=pwr
        attacked[si][sj] = True

    else:
        ## 포탄 공격
        arr[si][sj]-=pwr
        attacked[si][sj] = True
        for di,dj in (1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1),(1,-1),(-1,1):
            ni,nj = si-di,sj-dj

            if ni >= N:
                ni = N- ni
            if nj >= M:
                nj = M- nj

            if arr[ni][nj]<=0 or (ni, nj) == (wi, wj):
                continue
            arr[ni][nj]-=pwr//2 # 주변
            attacked[ni][nj] = True # 공격 당한 turn


    #포탄 부서짐


    # 공격과 무관 포탑 +1
    for i in range(N):
        for j in range(M):
            if arr[i][j]<=0:
                continue
            if attacked[i][j]== True:
                continue
            else:
                arr[i][j]+=1


    # 종료 조건
    cnt=N*M
    for i in range(N):
        for j in range(M):
            if arr[i][j]<=0:
                cnt-=1
    if cnt <=1:
        break


si,sj=strongest()
print(arr[si][sj])