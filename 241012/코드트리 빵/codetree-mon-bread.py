N,M=map(int,input().split())
bset=set()
arr=[list(map(int,input().split())) for _ in range(N)]
for i in range(N):
    for j in range(N):
        if arr[i][j]==1:
            bset.add((i,j))
store={}
for m in range(1,M+1):
    x,y=map(int,input().split())
    store[m]=(x-1,y-1)

players={}
stop=[0]*M # 인덱스 하나 빼서

#ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
from collections import deque
def bfs(si,sj,dests): # 최단 거리 동일 반경
    #TODO: 최단 거리에 만족되는 걸 찾으면, 동일 반경 다 찾고 반환-> 나중에 소팅 (벽이나 조건이 좀 까다로울 때 사용)
    v=[[0]*N for _ in range(N)]
    v[si][sj]=1
    q=deque([(si,sj)])
    tlst=[]

    while q:
        nq=deque()
        for ci,cj in q:
            if (ci,cj) in dests:
                tlst.append((ci,cj))
            else:
                for di,dj in ((0,1),(0,-1),(1,0),(-1,0)):
                    ni,nj=ci+di,cj+dj
                    if (0<=ni<N and 0<=nj<N and v[ni][nj]==0 and arr[ni][nj]!=-1):
                        v[ni][nj]=1
                        nq.append((ni,nj))

        if len(tlst)>0:
            tlst.sort()
            return tlst[0]
        q=nq

    return False


def find_step(m): # 바로 다음 스텝이 store일 수도
    pi,pj=players[m]
    si,sj=store[m]
    ei,ej=bfs(si,sj,((pi+1,pj),(pi-1,pj),(pi,pj+1),(pi,pj-1))) # 편의점에서 가장 가까운 위치 찾기
    return ei,ej

def go_to_basecamp(m):
    si,sj=store[m]
    ei,ej=bfs(si,sj,bset)
    return ei,ej


#==========================================
t=0
while True:
    # [1] 격자에 있는 사람들 이동
    sset=set()
    t += 1
    for m in range(1, M + 1):
        if t > m:
            if stop[m-1]: continue
            mi,mj=find_step(m)
            players[m] = [mi,mj]  # 이동

            if (mi,mj) == store[m]:
                sset.add((mi,mj))
                stop[m-1]=1

    if stop.count(0)==0:
        break

    # [2] 편의점 도착시 벽처리
    for wi,wj in sset:
        arr[wi][wj]=-1

    # [3] 자기 차례에 베이스캠프 도착
    for m in range(1,M+1):
        if t == m:
            if stop[m - 1]: continue
            mi,mj=go_to_basecamp(m)
            bset.remove((mi,mj)) # 못 가는 베이스캠프
            players[m]=[mi,mj] # 이동
            arr[mi][mj]=-1

print(t)