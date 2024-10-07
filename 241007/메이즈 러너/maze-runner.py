N,M,K=map(int,input().split())
arr=[list(map(int,input().split())) for _ in range(N)]
player=[]
for m in range(M):
    pi,pj = map(lambda x:int(x)-1,input().split())
    player.append([pi,pj,False,0]) # 플레이어 위치(i,j),out,d
    arr[pi][pj]-=1 # 사람

ei,ej=map(lambda x:int(x)-1,input().split())
Exit=[ei,ej]
arr[ei][ej]=-11

pflag=0
def pprint(arr1):
    print("\n".join(" ".join(f"{elem:>3}" for elem in layer) for layer in arr1))

# 초기 세팅
if pflag: print('\n')
if pflag: pprint(arr)

# [1] 참가자 이동
for turn in range(1,K+1):
    for m in range(M):
        # 참가자 좌표
        pi,pj,pout,pd=player[m]
        if pout: continue # 탈출 했으면
        ei,ej=Exit
        mn=abs(pi-ei)+abs(pj-ej) # 현재 거리
        mlst=[]
        for di,dj in ((1,0),(-1,0),(0,-1),(0,1)): # 상하 먼저 이동
            ni,nj=pi+di,pj+dj
            dist=abs(ni-ei)+abs(nj-ej)
            if 0<=ni<N and 0<=nj<N and arr[ni][nj]<=0: # 범위 내, 조건: 내구도 0 or 사람
                if mn>dist:
                    mn=dist
                    mlst=[ni,nj]
        # 이동 가능하면
        if len(mlst)>0:
            ni, nj = mlst
            pd += 1  # 이동하면 거리 한 칸 추가
            if mlst==Exit: # 출구면
                pout=True
                arr[pi][pj] += 1
                player[m] = [ni, nj, pout, pd]
                continue
            # 참가자 이동
            player[m] = [ni, nj, pout, pd]
            arr[pi][pj]+=1
            if pflag: print(f"---{turn}초:-------{m}번째 참가자 이동 전----------")
            if pflag: pprint(arr) # 이동 전
            arr[mlst[0]][mlst[1]]-=1
            if pflag: print(f"---{turn}초:-------{m}번째 참가자 이동 후----------")
            if pflag: pprint(arr)


    #[2] 미로 회전
    #[2-1] 가장 작은 정사각형 길이
    mn=N
    for m in range(M):
        pi,pj,pout,_ = player[m]
        if pout: continue
        if mn>max(abs(ei-pi),abs(ej-pj)):
            mn=max(abs(ei-pi),abs(ej-pj)) # 최소 길이 구하기
    mn+=1 # 이렇게 해줘야 함 좌표의 차이랑 실제 길이랑 다르니까?
    #[2-2] 참가자, 출구 포함한 정사각형 탐색
    ei, ej = Exit
    tlst = []
    for si in range(N - mn + 1):
        for sj in range(N - mn + 1):
            is_player,is_exit=0,0   # si,sj가 좌상단, 길이가 mn인 정사각형 탐색
            for i in range(mn):
                for j in range(mn):
                    ni,nj=si+i,sj+j
                    if (ni,nj)==(ei,ej):
                        is_exit=1
                    elif arr[ni][nj]<0 : # 사람
                        is_player=1
            if is_player and is_exit and len(tlst)==0 : # 둘 다 있으면
                tlst=[si,sj] # 좌상단 좌표, 참가자 좌표(들)
                break

    #[2-3] 정사각형 부분 회전 (시계방향 90도 회전) -> 위의 정사각형 회전, 출구, 사람 회전
    if pflag:print("\n")
    if pflag:print("----------회전 전------------")
    if pflag:pprint(arr)

    si,sj=tlst
    narr = [x[:] for x in arr]
    for i in range(mn):
        for j in range(mn):
            narr[si+i][sj+j]=arr[si+mn-1-j][sj+i]
            if narr[si+i][sj+j]>0: # 벽이면
                narr[si + i][sj + j]-=1 # 내구도 감소

    if pflag:print("----------회전 후------------")
    if pflag:pprint(narr)

    arr=narr
    if pflag:print("----------회전 후 arr update!------------")
    if pflag:pprint(arr)

    if pflag:print("-----------참가자, 출구 회전 전-------------")
    if pflag:print("플레이어",player)
    if pflag:print("출구",Exit)
    # 2-3-1 참가자, 출구 회전
    # 출구 회전
    i, j = ei - si, ej - sj
    ei, ej =  si + j, sj + mn - 1 - i
    Exit=[ei,ej] # 출구 업데이트
    # 참가자 회전
    for m in range(M):
        pi,pj,pout,_=player[m]
        if pout: continue
        if si<=pi<si+mn and sj<=pj<sj+mn: # 회전 사각형 내에 있으면
            # 회전 이동 (arr 이동은 위에서 해서 X)
            i,j=pi-si,pj-sj
            pi,pj= si + j, sj + mn - 1 - i
            player[m][:2]=[pi,pj]

    if pflag:print("-----------참가자, 출구 회전 후-------------")
    if pflag:print("플레이어",player)
    if pflag:print("출구",Exit)

total_d=0
for m in range(M):
    pd=player[m][-1]
    total_d+=pd
print(total_d)
ei,ej=Exit
print(ei+1,ej+1) # **** 좌표 출력할 때에는 원래 최좌측 상단 기준으로!!