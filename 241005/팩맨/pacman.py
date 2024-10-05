M,T=map(int,input().split())
pr,pc=map(int,input().split())
pm=(pr-1,pc-1)
arr_mon = [[[] for _ in range(4)] for _ in range(4)]
arr_dead=[[0]*4 for _ in range(4)] # 시체 맵

for _ in range(M):
    r,c,d=map(int,input().split())
    arr_mon[r-1][c-1].append(d-1)
dir_map={0:(-1,0),1:(-1,-1),2:(0,-1),3:(1,-1),4:(1,0),5:(1,1),6:(0,1),7:(-1,1)}
dead=[] #시체 배열

def in_range(i,j):
    return 0<=i<4 and 0<=j<4

for t in range(T):
    # [1] 몬스터 복제 시도
    ## 동일 방향 알 생성 => egg 배열에 위치, 방향 저장 -> 5에서 몬스터 배열(mon)과 몬스터 맵(arr_mon)에 저장
    # egg=[row for row in arr_mon] # mon 그대로 복제 =>이건 얕은 복사
    egg= [ [row[:] for row in layer] for layer in arr_mon ] #**

    # [2] 몬스터 이동
    ## 자기 방향 (mon)에서 찾고 해당 방향으로 이동-> 몬스터 시체 (arr_dead) or pm or not in_range -> d=(d+1)%8 하며 확인
    mv=[]
    for i in range(4):
        for j in range(4):
            if len(arr_mon[i][j])==0:
                continue
            for md in sorted(arr_mon[i][j],reverse=True):
                nd = md
                for _ in range(8):
                    ni, nj = i + dir_map[nd][0], j + dir_map[nd][1]
                    if not in_range(ni, nj) or arr_dead[ni][nj] > 0 or (ni, nj) == pm:  # 몬스터 시체(arr_dead) or pm or not in_range -> 45회전
                        nd = (nd + 1) % 8
                        continue
                    else:  # 진행 가능 -> 이동
                        # mon[i] = (ni, nj, nd)  # 방향 및 위치 업데이트
                        arr_mon[i][j].remove(md)  # 맵에 반영
                        mv.append((ni,nj,nd))
                        break
    for ni,nj,nd in mv:
        arr_mon[ni][nj].append(nd)  # 이러면 다음 턴에 돌 때 또 처리하게 됨 -> 다 돌고 마지막에

    # [3] 팩맨 이동 -> 3칸 이동 ## 이 부분에 대한 검증/ 더 나은 방법? => bfs로 경로 저장하는 법 또 까먹음// bfs 경로 저장, 달팽이 이런 기본적인 건 암기
    nr,nc=pm
    mx=0
    path=[]
    for d1i,d1j in (dir_map[0],dir_map[2],dir_map[4],dir_map[6]): # 상좌하우
        nr1,nc1=nr+d1i,nc+d1j
        if not in_range(nr1,nc1):
            continue
        cnt1=0
        if len(arr_mon[nr1][nc1])>0: # 몬스터 있으면
            cnt1=len(arr_mon[nr1][nc1])

        for d2i,d2j in (dir_map[0],dir_map[2],dir_map[4],dir_map[6]):
            nr2, nc2 = nr1 + d2i, nc1 + d2j
            if not in_range(nr2, nc2):
                continue
            cnt2=0
            if len(arr_mon[nr2][nc2])>0: # 몬스터 있으면
                cnt2=len(arr_mon[nr2][nc2])

            for d3i,d3j in (dir_map[0],dir_map[2],dir_map[4],dir_map[6]):
                nr3, nc3 = nr2 + d3i, nc2 + d3j
                if not in_range(nr3, nc3):
                    continue
                cnt3=0
                if  len(arr_mon[nr3][nc3])>0 and (nr3,nc3)!=(nr1,nc1):  # 몬스터 있으면
                    cnt3 = len(arr_mon[nr3][nc3])

                cnt=cnt1+cnt2+cnt3 #최종 잡은 수
                if cnt>mx:
                    mx=cnt
                    path=[(nr1,nc1),(nr2,nc2),(nr3,nc3)]
    # pm=(nr3,nc3) # path의 마지막을 업데이트 해야지
    pm=path[-1]
    # 경로 상 몬스터 제거 -> 시체 생성## ## dead가 더 많음
    if len(path)>1:
        for pi,pj in path:
            arr_dead[pi][pj]+=len(arr_mon[pi][pj]) # 시체로 투입
            dead.append((pi,pj,t+2,len(arr_mon[pi][pj]))) # 시체 위치, 소멸 턴 수, 시체 수(더해지는 걸 해야 하는데 기존에 있던 걸 넣음)
            pop_num=[]
            if len(arr_mon[pi][pj])>0:
                arr_mon[pi][pj] = []


    # [4] 몬스터 시체 소멸 -> arr_dead랑 dead 배열 둘 다 생각하기
    pop_num=[]
    for idx,(r,c,dead_turn,dnum) in enumerate(dead):
        if t==dead_turn: # 시체가 죽어야 하는 턴이면
            pop_num.append(idx)
            for i in range(4):
                for j in range(4):
                    if (i,j)==(r,c): #
                        if arr_dead[i][j]-dnum>=0:
                            arr_dead[i][j]-=dnum
                        else:
                            a=1
    pop_num.sort(reverse=True)
    for n in pop_num:
        dead.pop(n)

    # [5] 몬스터 복제 완성 [1] 에서 egg 배열에 추가했던 것들 mon배열과 arr_mon에 추가
    for i in range(4):
        for j in range(4):
            arr_mon[i][j]+=egg[i][j]


result=0
for i in range(4):
    for j in range(4):
        if arr_mon[i][j]:
            result+=len(arr_mon[i][j])
print(result)