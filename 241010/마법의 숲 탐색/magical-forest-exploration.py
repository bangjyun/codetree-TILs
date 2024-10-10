R,C,K=map(int,input().split())
team=[list(map(int,input().split())) for _ in range(K)] # 골렘 시작 열, 출구 방향
arr=[[1]+[0]*C+[1] for _ in range(R+3)]+[[1]*(C+2)]
ext=set()
p=1

#ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
from collections import deque
def bfs(arr,si,sj,tn): # 맵,정령 위치, 팀번호 넘겨서 가장 남쪽 행 반환 (mx+1) => 내 팀 번호면 이동 가능, >10 다른 팀일 때, 이전 좌표가 ext에 있었으면 이동 가능 (0 or 1 or 다른 팀 번호 불가)
    q=deque([(si,sj)])
    v=[[0]*(C+1) for _ in range(R+4)]
    v[si][sj]=1
    mx=0 # 최대 남쪽 행
    while q: # 네방향,미방문,조건: 동일 팀, or 다른 팀 + 이전 좌표가 출구
        ci,cj= q.popleft()
        if ci > mx:
            mx = ci  # 최대 행 업데이트

        for di,dj in ((1,0),(0,-1),(0,1),(-1,0)):
            ni,nj=ci+di,cj+dj
            if arr[ni][nj]==1:
                continue
            if v[ni][nj] ==0 and  ((arr[ni][nj] == arr[ci][cj]) or (arr[ni][nj]>10 and (ci,cj) in ext)):
                q.append((ni,nj))
                v[ni][nj] = 1

    return mx+1 # 최대 '행'

tn=10
ans=0
while team: # 남은 골렘 있는 동안 진행
    tn+=1 # 팀번호 업데이트
    t=team.pop(0)
    tj,td=t
    ti=1  # 시작 중심 좌표, 출구 방향
    tdi=[-1,0,1,0]
    tdj=[0,1,0,-1]

    # [1] 골렘 이동 시작
    while True:
        # [1-1] 남쪽 이동
        if arr[ti+1][tj-1]==0 and arr[ti+1][tj+1]==0 and arr[ti+2][tj]==0: # 남쪽 이동 가능
            ti,tj=ti+1,tj
            continue
        # [1-2] 서남쪽 이동
        elif arr[ti-1][tj-1]==0 and arr[ti][tj-2]==0 and arr[ti+1][tj-1]==0 and arr[ti+1][tj-2]==0 and arr[ti+2][tj-1]==0: # 서쪽 이동 가능
            ti, tj = ti + 1, tj-1
            td=(td-1)%4
            continue
        # [1-2] 동남쪽 이동
        elif arr[ti - 1][tj +1] == 0 and arr[ti][tj + 2]==0 and arr[ti + 1][tj + 1]==0 and arr[ti + 1][tj +2]==0 and arr[ti + 2][tj + 1]==0:  # 동쪽 이동 가능
            ti, tj = ti + 1, tj + 1
            td=(td+1)%4
            continue
        else: # 더 이상 이동 불가
            if ti<4: # 골렘의 몸 일부 out?
                arr=[[1]+[0]*C+[1] for _ in range(R+3)]+[[1]*(C+2)]
                ext=set()
                break

            # [2] 정령 이동 (bfs)
            for ni,nj in ((ti,tj),(ti+1,tj),(ti-1,tj),(ti,tj+1),(ti,tj-1)):
                arr[ni][nj]=tn # 골렘 팀번호에 맞게 맵에 표시 (골렘 위치는 확정)

            ei,ej=ti+tdi[td],tj+tdj[td]
            ext.add((ei,ej)) # 출구 좌표들 한 번에 저장
            mx_row=bfs(arr,ti,tj,tn)-3 # 맵,정령 위치, 팀번호 넘겨서 가장 남쪽 행 반환 (mx+1)
            # print(mx_row)
            ans+=mx_row # 최종 행 누적 업데이트
            break

print(ans)