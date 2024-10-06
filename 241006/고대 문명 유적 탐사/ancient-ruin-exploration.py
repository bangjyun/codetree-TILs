L,N=3,5 #3x3
K,M =map(int,input().split())
arr=[]
for _ in range(5):
    arr.append(list(map(int,input().split())))
num=list(map(int,input().split()))

from collections import deque
def bfs(board):
    val=0
    for si in range(N):
        for sj in range(N):
            v = [[0] * N for _ in range(N)]
            v[si][sj]=1
            q=deque([(si,sj)])
            trace = deque([(si, sj)])
            dir=[(0,1),(0,-1),(1,0),(-1,0)]
            while q:
                ci,cj=q.popleft()
                for d in dir:
                    ni,nj=ci+d[0],cj+d[1]
                    if 0 <= ni < N and 0 <= nj < N and v[ni][nj]== 0 and board[ni][nj]>0:
                        v[ni][nj]=1
                        if board[ni][nj]==board[ci][cj]:
                            trace.append((ni,nj))
                            q.append((ni,nj))
            if len(trace)>=3:
                for ti,tj in trace:
                    board[ti][tj]=0
                val+=len(trace)

    return val,board

def rotate(board,r,si,sj):
    for k in range(r):
        narr = [x[:] for x in arr]
        for i in range(L):
            for j in range(L):
                board[si+i][sj+j]=narr[si+L-1-j][sj+i]
    return board

for turn in range(1,K+1):
    mx=0
    mx_board=()
    # 탐사 진행
    for r in range(1,4):
        for sj in range(3):
            for si in range(3):
                board=[x[:] for x in arr]
                board = rotate(board,r,si,sj)
                val,board=bfs(board) # 다 지운 후 돌려줌
                if mx<val:
                    mx_board=(si,sj,board) # 최적의 조합 (돌리는 중심, 돌리는 각)
                    mx=val
    # 획득을 못할 경우 종료
    if mx==0:
        break

    # 유물 획득
    si,sj,arr=mx_board

    # 유적 넣기
    for j in range(N):
        for i in range(N-1,-1,-1):
            if arr[i][j]==0:
                n=num.pop(0)
                arr[i][j]=n

    while True:
        val,_=bfs(arr)
        mx+=val
        for j in range(N):
            for i in range(N - 1, -1, -1):
                if arr[i][j] == 0:
                    n = num.pop(0)
                    arr[i][j] = n

        if val==0:
            break

    print(mx,end=" ")