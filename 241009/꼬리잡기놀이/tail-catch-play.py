N,M,K=map(int,input().split())
arr=[list(map(int,input().split())) for _ in range(N)]

def dfs(si,sj,tidx,flag):
    di=[1,-1,0,0]
    dj=[0,0,1,-1]
    global cnt
    if flag: # 몇 번째인지 찾는 flag
        v[si][sj] = 1
        for i in range(4):
            ni, nj = si + di[i], sj + dj[i]
            if 0 <= ni < N and 0 <= nj < N and v[ni][nj] == 0:
                v[ni][nj] = 1
                if arr[ni][nj] == tidx: # 우리 팀
                    cnt+=1 #
                    if (ni,nj) == fset: # 맞은 애
                        return False
                    dfs(ni, nj, tidx, 1)

    else:  # 팀번호 찾는 flag
        arr[si][sj]=tidx
        v[si][sj] = 1
        for i in range(4):
            ni,nj=si+di[i],sj+dj[i]
            if 0<=ni<N and 0<=nj<N and v[ni][nj]==0:
                v[ni][nj]=1
                if arr[ni][nj]==2:
                    arr[ni][nj]=tidx
                    dfs(ni,nj,tidx,0)
                elif arr[ni][nj]==3:
                    arr[ni][nj] = tidx
                    team[tidx].append((ni,nj))
                    return False

team={} # 팀의 머리, 꼬리만 저장
tidx=11
v = [[0] * N for _ in range(N)]
for i in range(N):
    for j in range(N):
        if arr[i][j]==1:
            team[tidx]=[(i,j)]
            dfs(i,j,tidx,0) # 팀을 다 팀 아이디로!
            tidx+=1

#ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
tot_score=0
for turn in range(K):
    # [1] 머리 방향 이동
    for tidx in range(11,11+M): # 모든 팀 이동
        si,sj=team[tidx][0] # head
        ei,ej=team[tidx][1] # tail

        di = [1, -1, 0, 0]
        dj = [0, 0, 1, -1]
        for i in range(4):
            ni, nj = ei + di[i], ej + dj[i]
            if 0 <= ni < N and 0 <= nj < N and arr[ni][nj]==tidx: # 범위 내, 우리 팀
                team[tidx][1]=(ni,nj) # 꼬리 업데이트
                arr[ei][ej] = 4  # 꼬리 이동

        for i in range(4):
            ni, nj = si + di[i], sj + dj[i]
            if 0 <= ni < N and 0 <= nj < N and arr[ni][nj]==4: # 길이 보임
                team[tidx][0] = (ni, nj)  # 꼬리 업데이트
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
    hit_team=0
    fset=() # 맞은 사람 좌표
    score=0

    v = [[0] * N for _ in range(N)]
    for i in range(N): # start에서 공 던지기
        ni, nj = si + dir[0] * i, sj + dir[1] * i
        if arr[ni][nj]>10: # 누가 맞음
            hit_team=arr[ni][nj] # 맞은 팀 인덱스
            fset=(ni,nj) # 최초에 만나는 사람
            cnt = 1  #
            head,tail = team[hit_team][0],team[hit_team][1]
            dfs(head[0],head[1], hit_team,1)
            score = cnt ** 2
            team[hit_team][0],team[hit_team][1]=tail,head # 맞은 팀 방향 바꾸기
            break
    tot_score+=score
print(tot_score)