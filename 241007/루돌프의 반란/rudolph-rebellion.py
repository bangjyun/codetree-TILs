'''
코드트리 루돌프의 반란 2회차
'''

#---------------------------------------------------
pflag=0
N, M, P, C, D=map(int,input().split())
arr=[[0]*N for _ in range(N)] # 산타 번호, 루
rou=list(map(lambda x: int(x)-1,input().split()))
arr[rou[0]][rou[1]]=-1
santa={}
for _ in range(P):
    m,si,sj=map(int,input().split())
    santa[m]=[si-1,sj-1,0,False,0] # 산타 위치, 점수, 탈락 여부, 기절 깨는 턴
    arr[si-1][sj-1]=m

def pprint(arr):
    print('\n'.join(' '.join(f"{elem:>2}" for elem in layer) for layer in arr))

############ 이거 완벽히 이해하고 다시 쓰기 -> 얘만 시간 또 잡아먹음 --------------
def bfs(): # 루에서 가까운 산(탈락 안한) 동일 반경 최소 거리, 유클리드, tlst 정렬 후 가장 가까운 목표산타 거리 반환 함수
    tlst=[]
    for m in range(1,P+1):
        si,sj,_,sout,_=santa[m]
        if sout==False:
            tlst.append([si,sj])
    tlst.sort(key=lambda x:(dist(x[0],x[1]),-x[0],-x[1]))
    if tlst[0][1]>49:
        a=1
    return tlst[0]

def in_range(i,j):
    return 0<=i<N and 0<=j<N
def dist(i,j):
    return (i-rou[0])**2+(j-rou[1])**2

# -----------여기서 한 시간 넘게 쓴 듯-> 처음 보는 구현? => 반드시 손코딩 우선
def communicate(sidx,di,dj):
    tmp = [sidx]
    while True:
        t = tmp.pop(0)
        ti, tj, tscore, tout, tturn = santa[t]  # 가야 하는 위치(ti,tj)
        if not in_range(ti, tj):
            tout = True
            if pflag: print("범위 밖!!!")
            if pflag:pprint(arr)
            santa[t] = [ti, tj, tscore, tout, tturn]
            break

        if arr[ti][tj] > 0:  # 가야 하는 위치에 다른 산타가 있는 경우
            if pflag:print("다른 산타 발견!!!")
            if pflag:pprint(arr)
            tidx=arr[ti][tj]
            tti,ttj,_,_,_=santa[tidx]
            tti,ttj=tti+di,ttj+dj # 원래 있던 애는 그 다음
            santa[tidx][0],santa[tidx][1]= tti,ttj # 목표 위치

            tmp.append(arr[ti][tj])
            arr[ti][tj] = t
            if pflag:print("내가 들어옴!!!")
            if pflag:pprint(arr)
            if pflag:print("tmp에 기존 산타 담음",tmp)

        else: # 아무도 없으면 내가!
            arr[ti][tj] = t
            if pflag:print("------아무도 없다-----------")

        santa[t] = [ti, tj, tscore, tout, tturn]
        if len(tmp) == 0: # 더 이상 움직 산타X
            break

# ========================================================
for turn in range(1,M+1):
    if turn ==6:
        a=1
    # 루돌프 이동 =============================
    if pflag:print("\n",f"======={turn}번째 턴==========")
    if pflag:pprint(arr)
    si,sj=bfs()
    ri,rj=rou
    di,dj=0,0 # 산이랑 가까워지게 이동
    if si>ri:   di=1
    elif si<ri: di=-1
    if sj>rj:   dj=1
    elif sj<rj: dj=-1
    if pflag:print("루돌프",ri,rj,"---목표산타---:",si,sj,"이동 방향:",di,dj)

    ni,nj=ri+di,rj+dj
    rou=(ni,nj)
    # 루 이동!
    if (ni,nj)==(si,sj): # 루-산 충돌
        if pflag:print("=======루-산 충돌=========")
        if pflag:pprint(arr)
        sidx=arr[si][sj]
        ci,cj,cscore,cout,cturn= santa[sidx]
        cscore+=C
        ci,cj=si+C*di,sj+C*dj
        if not in_range(ci,cj):
            cout=True
        cturn=turn+2
        if pflag:print("--------산타 충돌 전 상태(i,j,점수,탈락,기절 깨는턴)---------")
        if pflag:print(santa[sidx])
        santa[sidx]=[ci,cj,cscore,cout,cturn]
        if pflag:print("--------산타 충돌 후 상태(i,j,점수,탈락,기절 깨는턴)---------")
        if pflag:print(santa[sidx])

        # 산 - 상호작용 arr은 이때 업데이트
        if pflag:print("--------상호작용 전--------")
        if pflag:pprint(arr)
        communicate(sidx,di,dj)
        if pflag:print("--------상호작용 후--------")
        if pflag:pprint(arr)
    arr[ri][rj]=0
    arr[rou[0]][rou[1]] = -1

    # 산타 이동
    for idx in range(1,P+1):
        if pflag:print(f"--{idx}번째 산타 이동 전")
        if pflag:pprint(arr)
        ci, cj, cscore, cout, cturn = santa[idx]
        if cout==True or (cturn>turn):
            continue
        arr[ci][cj]=0
        md=(0,0)
        mn=dist(ci,cj) # 현재 기준 루와의 거리
        if mn==1:
            ri, rj = rou
            md=(ri-ci,rj-cj)
        else:
            ri, rj = rou
            for d in ((-1,0),(0,1),(1,0),(0,-1)): # 상우하좌
                ni,nj=ci+d[0],cj+d[1]
                if in_range(ni,nj) and dist(ni,nj)<mn and arr[ni][nj]==0: # 다른 산타 없음
                    mn=dist(ni,nj)
                    md=d # 최소가 되는 방향
        ci,cj=ci+md[0],cj+md[1]

        if (ci,cj)==(rou[0],rou[1]): # 충돌
            cturn=turn+2 # 기절
            cscore+=D
            ni,nj=ci-D*md[0],cj-D*md[1] # 이동 반대 방향
            ci,cj=ni,nj
            santa[idx]=[ci, cj, cscore, cout, cturn]
            if pflag:print("루-산 충돌!!! - 기절 산타",santa[idx],"현재 턴",turn)
            communicate(idx,-md[0],-md[1])

        else:
            arr[ci][cj]=idx # 루 없으면 그냥 이동
            santa[idx] = [ci, cj, cscore, cout, cturn]
            if pflag: print(f"--{idx}번쨰 산타 이동 후")
            if pflag: pprint(arr)

    out_cnt=0
    for m in range(1, P + 1):
        i,j,score,out,turn=santa[m]
        if not out:
            score+=1
        else: out_cnt+=1
        santa[m]=[i,j,score,out,turn]

    if out_cnt==P: # 다 탈락
        break

for m in range(1,P+1):
    print(santa[m][2],end=" ")