M, S = map(int, input().split())
fish = []
si,sj = map(int, input().split())
for _ in range(M):
    i,j,dr = map(int, input().split())
    # [0]:i, [1]:j, [2]:dr, [3]:cnt: 군집크기
    fish.append([i-1,j-1,dr-1,1])

si,sj = si-1,sj-1
v = [[0]*4 for _ in range(4)]   # 물고기 냄새 표시
boundary = set([(i,j) for j in range(4) for i in range(4)])

#      ←,↖, ↑,↗, →,↘, ↓, ↙  : 시계 방향 => 반대로(반시계) 체크
di = [ 0,-1,-1,-1, 0, 1, 1, 1]
dj = [-1,-1, 0, 1, 1, 1, 0,-1]

def move_fish():
    # 상어X, 범위내, 냄새X, 반시계 45도
    for i in range(len(fish)):
        ci,cj,dr,cnt=fish[i]
        # 반시계방향(감소방향)으로 8방향체크(현재방향부터)
        for k in range(8):
            ni,nj=ci+di[(dr-k)%8], cj+dj[(dr-k)%8]
            # 범위체크를 먼저진행하고 v[] 등 확인
            if (ni,nj)!=(si,sj) and (ni,nj) in boundary and v[ni][nj]==0:
                fish[i]=[ni,nj,(dr-k)%8,cnt]
                break

def shark():
    # [3-1] 상어 3칸 연속이동, 상어위치
    mx = -1                     # 무조건 갱신될 최악의 값으로 초기화!
    del_set=set()
    for d1 in (2,0,6,4):        # 상->좌->하->우
        i1,j1=si+di[d1], sj+dj[d1]
        if (i1,j1) not in boundary: continue    # 범위밖이면 다음방향으로...
        for d2 in (2,0,6,4):    # 상->좌->하->우
            i2,j2=i1+di[d2], j1+dj[d2]
            if (i2,j2) not in boundary: continue    # 범위밖이면 다음방향으로...
            for d3 in (2,0,6,4):    # 상->좌->하->우
                i3,j3=i2+di[d3], j2+dj[d3]
                if (i3,j3) not in boundary: continue    # 범위밖이면 다음방향으로...

                fcnt = 0
                shk_set = set(((i1,j1),(i2,j2),(i3,j3)))
                for i,j,dr,cnt in fish:
                    if (i,j) in shk_set:    # 상어의 3위치와 같은 좌표면
                        fcnt+=cnt
                if mx<fcnt:
                    mx,ni,nj = fcnt,i3,j3
                    del_set=shk_set         # 삭제할 좌표 후보

    # [3-2] 물고기 삭제 전 냄새(3) 남김
    for i in range(len(fish)-1,-1,-1):      # 삭제는 반대로 접근이 편리
        if (fish[i][0],fish[i][1]) in del_set:
            v[fish[i][0]][fish[i][1]]=3
            fish.pop(i)

    return ni,nj    # 상어의 최종좌표 리턴

def merge(fish):
    # 같은좌표, 같은방향의 물고기 군집 누적
    fish.sort(key=lambda x:(x[0],x[1],x[2]))

    i=1
    while i<len(fish):
        if fish[i-1][:3]==fish[i][:3]:  #  위치,방향 같으면
            fish[i-1][3]+=fish[i][3]
            fish.pop(i)
        else:
            i+=1

for _ in range(S):              # S턴만큼 처리
    # [1] 물고기 복제마법
    fish_n = [x[:] for x in fish]

    # [2] 모든 물고기 한칸 이동
    move_fish()

    # [3] 상어 3칸 연속이동, 상어위치 물고기삭제 및 냄새남김(3)
    si,sj=shark()

    # [4] 물고기냄새 -1
    for i in range(4):
        for j in range(4):
            if v[i][j]>0:
                v[i][j]-=1

    # [5] 복제된 물고기와 기존물고기 합치기
    fish+=fish_n
    merge(fish)         # 같은좌표,방향의 물고기 군집개수를 합치고 삭제

ans=0
for i in range(len(fish)):
    ans+=fish[i][3]
print(ans)