from collections import deque

N,M = map(int,input().split())
arr=[]
for i in range(N):
    arr.append(list(map(int,input().split())))


goal=[[-1,-1]]*(M+1) # 편의점 좌표
for i in range(1,M+1):
    goal[i]=list(map(lambda x:int(x)-1,input().split()))


man=[(-1,-1)]*(M+1)
is_stop=[False]*(M+1)


def in_range(i,j):
    return 0<=i<N and 0<=j<N

def go_to_nextstep(si,sj,ei,ej):
    q = deque()
    q.append((si,sj))
    # v = [[] * N for _ in range(N)]
    v = [[[] for _ in range(N)] for _ in range(N)] ##
    v[si][sj]=(si,sj)
    path=[]
    while q:
        ci,cj=q.popleft()
        if (ci,cj)==(ei,ej):
            if v[ci][cj] == (si, sj): # 편의점 바로 전
                return ei,ej

            while True:
                ci,cj=v[ci][cj]
                if (ci,cj)==(si,sj):
                    i,j=path[::-1][0]
                    return i,j
                path.append((ci,cj))

        for di,dj in (-1,0),(0,-1),(0,1),(1,0): # 상좌우하
            ni,nj=ci+di,cj+dj
            if in_range(ni, nj) and arr[ni][nj] >= 0 and len(v[ni][nj])==0:
                q.append((ni, nj))
                v[ni][nj] = (ci,cj)

    return False

def find_basecamp(si,sj):
    q=deque()
    q.append((si,sj))
    visited=[[False]*N for _ in range(N)]

    while q:
        ci,cj=q.popleft()
        for di,dj in (-1,0),(0,-1),(0,1),(1,0): # 행 작고 열 작게
            ni,nj=ci+di,cj+dj
            if in_range(ni,nj) and arr[ni][nj]>=0 and visited[ni][nj]==False:
                if arr[ni][nj]==1: # 베캠
                    return ni,nj
                q.append((ni,nj))
                visited[ni][nj]=True

    return False


t=0
while True:
    t+=1
    ns= [(-1,-1)]*(M+1)
    for m in range(1,M+1):
        if is_stop[m]:
            continue
        if m<t:
            # 1번 행동 bfs 적용해 편의점 최단 경로쪽 한칸 이동 -> 상,좌,우,하
            gi, gj = goal[m]
            si,sj=man[m]
            ni,nj = go_to_nextstep(si,sj,gi,gj)
            man[m] = (ni,nj) # 이동
            # 2번 행동 : 편의점 도착하면 is_stop
            if (gi,gj)==(ni,nj):
                is_stop[m]=True
                ns[m]=(ni,nj)
                # arr[ni][nj] = -1

        elif m==t:
            gi,gj=goal[m]
            # 가까운 베캠 찾기 (bfs) -> 행작은, 열작은
            ni,nj  = find_basecamp(gi, gj)
            # 베이스캠프로 이동 후 -1처리로 칸 블록
            man[m]=(ni,nj)
            ns[m] = (ni, nj)
            # arr[ni][nj] = -1

    for m in range(1,M+1):
        ni,nj=ns[m]
        arr[ni][nj] = -1

    if is_stop.count(True)==M:
        print(t)
        break