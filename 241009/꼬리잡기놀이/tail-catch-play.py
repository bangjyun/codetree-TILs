N,M,K=map(int,input().split())
arr=[list(map(int,input().split())) for _ in range(N)]

def pprint(arr):
    print("\n".join(" ".join(f"{elem:>3}" for elem in l) for l in  arr))
p=1
from collections import deque
def bfs(si,sj,tidx): # 자기 팀 만드는 함수
    v=[[0]*N for _ in range(N)]
    v[si][sj]=1
    q=deque([(si,sj)])
    team[tidx]=[(si,sj)]
    di = [1, -1, 0, 0]
    dj = [0, 0, 1, -1]
    flag=0
    while q:
        ci,cj=q.popleft()
        arr[ci][cj] = tidx # 머리
        for i in range(4):
            ni, nj = ci + di[i], cj + dj[i]
            if 0<=ni<N and 0<=nj<N and v[ni][nj]==0:
                if arr[ni][nj]==2: # 몸통
                    team[tidx].append((ni,nj))
                    q.append((ni,nj))
                    arr[ni][nj] = tidx
                    v[ni][nj] = 1 # 나중에 방문할 곳은 1처리 하면 안 됨
                    flag=1
                     # 만약 2만 있는 쪽으로 탐색하다가 2가 없으면 3을 가려 한다? --> 2 만나면 break
                elif flag and arr[ni][nj]==3:
                    team[tidx].append((ni, nj))
                    arr[ni][nj] = tidx


team={} # 팀 전체 저장
tidx=11
v = [[0] * N for _ in range(N)]
for i in range(N):
    for j in range(N):
        if arr[i][j]==1:
            bfs(i,j,tidx) # 팀을 다 팀 아이디로!
            tidx+=1
#ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
tot_score=0
for turn in range(K):
    for tidx in range(11,11+M): # 모든 팀 이동
        # [1] 머리 방향 이동
        si,sj=team[tidx][0] # head

        di = [1, -1, 0, 0]
        dj = [0, 0, 1, -1]

        ti,tj=team[tidx].pop() # 꼬리 pop
        arr[ti][tj]=4 # 꼬리 이동
        # 머리 이동
        for i in range(4):
            ni, nj = si + di[i], sj + dj[i]
            if 0 <= ni < N and 0 <= nj < N and arr[ni][nj]==4: # 길이 보임
                team[tidx].insert(0, (ni, nj))
                arr[ni][nj] = tidx  # 머리 업데이트

    # [2] 공 던지기
    if 0 <= turn % (4 * N) < N:
        start, dir = (turn % N, 0), (0, 1)
    elif N <= turn % (4 * N) < 2 * N:
        start, dir = (N - 1, turn % N), (-1, 0)
    elif 2 * N <= turn % (4 * N) < 3 * N:
        start, dir = (N - 1 - turn % N, N - 1), (0, -1)
    elif 3 * N <= turn % (4 * N) < 4 * N:
        start, dir = (0, N - 1 - turn % N), (1, 0)

    si, sj = start
    hit_team = score = k = 0

    for i in range(N): # start에서 공 던지기
        ni, nj = si + dir[0] * i, sj + dir[1] * i
        if arr[ni][nj] > 10:  # 누가 맞음
            hit_team=arr[ni][nj] # 맞은 팀 인덱스
            k=team[hit_team].index((ni,nj))+1
            # 머리 꼬리 변경
            team[hit_team]=team[hit_team][::-1]  # 맞은 팀 방향 바꾸기
            tot_score += k**2
            break

print(tot_score)