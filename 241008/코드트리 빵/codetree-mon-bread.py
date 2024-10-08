N,M=map(int,input().split())
arr=[list(map(int,input().split())) for _ in range(N)] # 베이스캠프랑 벽만 존재
store=[list(map(lambda x:int(x)-1,input().split())) for _ in range(M)]
i=0
for s in store:
    i+=1
player=[[N]*2 for _ in range(M+1)]
stop=[0]*(M+1)
stop[0]=1

p=0
#================================================================================
def pprint(arr):
    print("\n".join(" ".join(f"{elem:>3}" for elem in layer) for layer in arr))

from collections import deque

def bfs1(pi,pj,idx): # pi,pj부터 편의점까지의 최소 dist 반환->편의점 만나면 리턴
    v=[[0]*N for _ in range(N)]
    q=deque([(pi,pj)])
    v[pi][pj]=1
    si,sj=store[idx-1] # 목표 편의점!
    dist=0
    while q:
        ci,cj=q.popleft()
        for di,dj in ((-1,0),(0,1),(0,-1),(1,0)):
            ni,nj=ci+di,cj+dj
            if 0<=ni<N and 0<=nj<N and v[ni][nj]==0 and arr[ni][nj]!=-1:
                v[ni][nj] = v[ci][cj] + 1
                # if p: print("++++++++탐색+++++++++")
                # if p: pprint(v)
                if (ni,nj)==(si,sj):  # 목표 편의점!!
                    dist=v[ni][nj]-1 # 1부터 시작했으니까 1 빼줘서 반환
                    if p: print("편의점",si,sj,"시작점",pi,pj  ,"거리",dist)
                    return dist
                q.append((ni,nj))

def bfs2(si,sj,idx): # 가장 가까운 베이스캠프 ,행작, 열작
    v = [[0] * N for _ in range(N)]
    q = deque([(si, sj)])
    v[si][sj] = 1
    blst=[]
    while q:
        nq=deque()
        for ci,cj in q:
            for di, dj in ((-1, 0), (0, 1), (0, -1), (1, 0)):
                ni, nj = ci + di, cj + dj
                if 0 <= ni < N and 0 <= nj < N and v[ni][nj] == 0 and arr[ni][nj] != -1:
                    v[ni][nj] = v[ci][cj] + 1
                    if arr[ni][nj]==1: # 베이스캠프 발견
                        blst.append((ni,nj))# 가까운 베이스 캠프 좌표 저장
                    nq.append((ni,nj))
        q=nq
        if len(blst)>0:
            blst.sort() # 행작>열작
            return blst[0]


def find_basecamp(idx):
    si,sj=store[idx-1]
    bi,bj=bfs2(si,sj,idx)
    # 플레이어 베이스캠프로 이동
    pi,pj=player[m]
    player[m]=[bi,bj]
    # 이동 불가 처리
    arr[bi][bj]=-1
    return bi,bj # 가장 가까운 베캠 반환

def find_store_step(idx): # 이상
    pi,pj=player[idx]
    si,sj=store[idx-1]
    mlst=[]
    mn=N*2
    # 목적지까지의 거리가 최소가 되는 step!!
    for di,dj in ((-1,0),(0,-1),(0,1),(1,0)):
        ni,nj=pi+di,pj+dj
        # 4방향 중 하나가 목적지일 때!! => 이거 놓침
        if (ni,nj)==(si,sj):
            mlst=[ni,nj]
            break
        if 0<=ni<N and 0<=nj<N and arr[ni][nj]!=-1:
            dist = bfs1(ni,nj,idx) # 가장 가까운 스토어로의 발걸음
            if dist:
                if mn>dist:
                    mn=dist
                    mlst=[ni,nj]

    return mlst

#----------------------------------------------
turn=0
while True:
    turn += 1 # turn의 업데이트는 처음에!
    if p: print(f"==================={turn}턴=======================")
    for m in range(1,M+1):
        if p: print(f"=======시작 {m} 번째 사람=========")
        if stop[m]==1: continue
        if turn>m:
            #[1] 편의점 이동
            if p: print("편의점",store[m-1])
            if p: print("이동 전",player[m])
            ni,nj= find_store_step(m)
            player[m]=[ni,nj]
            if p: print(ni, nj, "편의점으로 이동")
            if p: print("이동 후",player[m])

            if [ni,nj]==store[m-1]: # 편의점 도착
                stop[m]=1 # 그 플레이어는 멈춤
                arr[ni][nj] = -1  # 이동 불가
                if p: print(f"=======편의점 도착 -> {m}번 플레이어=======")
                if p: pprint(arr)

        elif turn==m:
            ni,nj=find_basecamp(m) # 편의점과 가까운 베이스캠프 좌표
            if p: print(ni,nj,"베이스 캠프로 이동")
            player[m] =[ni, nj]
            arr[ni][nj] = -1  # 이동 불가
            if p: print(f"======={m}번 플레이어 -> 베이스캠프 도착=======")
            if p: pprint(arr)

    if stop.count(1) == M+1: break  # 모두 도착했으면

print(turn)