from collections import deque
# import sys

# 표준 입력을 input.txt 파일로 리디렉션
# sys.stdin = open("input.txt", "r")

N,M,K=map(int,input().split())
board=[]
for _ in range(N):
    board.append(list(map(int,input().split())))
a=1

def in_range(i,j):
    return 0<=i<N and 0<=j<N

## [1] 객체 생성
class Team:
    def __init__(self):
        self.coords=[]
        self.path=[]
        self.dir=1

    def get_score(self,k):
        global tot_score
        a,b=((k)//N)%4,(k)%N
        direction={0:(0,1),1:(-1,0),2:(0,-1),3:(1,0)}
        start={0:(b,0),1:(N-1,b),2:(N-1-b,N-1),3:(0,N-1-b)}
        d=direction[a] # 공 던지는 방향
        s=start[a] # 공 던지는 위치
        ni,nj=s[0],s[1]
        k_person=None
        # 2-1 공 던지기 (dir에 맞게 coords 업데이트),
        for i in range(N):
            if not in_range(ni,nj): # 사실 필요 없음
                break
            if 1<=board[ni][nj]<=3 and ((ni,nj) in self.coords): # 팀원 중 한 명 만나면 해당 좌표 받고 끝
                k_person=(ni,nj)
                break
            ni,nj=ni+d[0],nj+d[1]
        # 2-2 점수 얻기
        k_score=0
        if k_person is not None:
            k_score=self.coords.index(k_person)+1
            tot_score+=k_score**2
            ### 2-3 방향 바꾸기 (dir 변경, coords 1과 4 변경
            self.coords[0], self.coords[-1] = self.coords[-1], self.coords[0]  # H<->T
            self.dir= - self.dir # 방향 바꾸기

    def move(self):
        for i,c in enumerate(self.coords): # board update도 해줘야 함
            idx=self.path.index(c) # path상 위치
            num=board[c[0]][c[1]]
            board[c[0]][c[1]]=4
            nidx=(idx+self.dir)%len(self.path)
            self.coords[i]=self.path[nidx]
            board[self.coords[i][0]][self.coords[i][1]]=num


def get_path(i,j):
    queue=deque()
    queue.append((i,j))
    path=deque([(i,j)])
    coord=[(i,j)]
    v=[[0]*N for _ in range(N)]
    dx=[0,-1,0,1]
    dy=[-1,0,1,0]

    while queue:
        ti,tj=queue.popleft()
        v[ti][tj]=1
        if not in_range(ti,tj):
            break
        for i in range(4):
            ni,nj=ti+dx[i],tj+dy[i]
            if in_range(ni,nj) and v[ni][nj]==0: # 방문한 적 없고, 범위 내
                if board[ni][nj]==4:  # 4 먼저 넣고
                    queue.append((ni,nj))
                    path.append((ni, nj))
                    break
                elif board[ni][nj]>1:  # 그 다음 3,2 => 이렇게 하니까 왜 coord가 제대로 순서대로 담기지..?

                    queue.append((ni, nj))
                    path.append((ni, nj))
                    coord.append((ni, nj))
                    break
                elif board[ni][nj] == 1:  # 마지막 1을 만나면 넣지 않고 초기화
                    queue=deque() # 큐에 있는 거 다 없애기
                    break
    path.reverse()
    return path,coord



# [1] 팀 객체 생성
Teams=[]
for i in range(N):
    for j in range(N):
        if board[i][j]==1:
            p,c=get_path(i,j) # bfs
            # 객체 생성
            t=Team()
            t.path=p
            t.coords=c
            Teams.append(t)

## [2] 시뮬 시작
tot_score=0
for k in range(K):
    for team in Teams:
    ### 2-1 한 칸 이동
        team.move()
    ### 2-2  점수 얻기 (get_score(k)) (+ 맞으면 방향 바꾸기)
        team.get_score(k)
print(tot_score)
# return tot_score