N,M,K=map(int,input().split())
gun=[list(map(int,input().split())) for _ in range(N)] # 2개인 것만 리스트로
for i in range(N):
    for j in range(N):
        gun[i][j]=[gun[i][j]]
        if gun[i][j][0]==0:
            gun[i][j].remove(0)

player={}
arr=[[0]*N for _ in range(N)] # 플레이어 인덱스
points=[0]*(M+1)

for m in range(1,M+1): #1~M+1
    x,y,d,s = map(int,input().split())
    player[m]=[x-1,y-1,d,s,0] # x,y,방향,초기 공격력, 보유 총
    arr[x-1][y-1]=m

def in_range(i,j):
    return 0<=i<N and 0<=j<N
#ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
dir={0:(-1,0),1:(0,1),2:(1,0),3:(0,-1)}
op={0:2,1:3,2:0,3:1}

for turn in range(1,K+1):
    for m in range(1,M+1):
        try:
            pi,pj,pd,ps,pgun = player[m]
        except:
            a=1
        # [1] 방향으로 이동
        ni,nj=pi+dir[pd][0],pj+dir[pd][1]
        if not in_range(ni,nj):
            pd=op[pd] # 방향 전환
            player[m] = pi, pj, pd, ps, pgun # 업데이트
            ni, nj = pi + dir[pd][0], pj + dir[pd][1]
        arr[pi][pj]=0 # 원래 자리 비움
        # pi,pj=ni,nj
        # arr[ni][nj]=m # 이동 => 뒤에서 해줘야 함

        # [2] 플레이어 확인
        if arr[ni][nj]: # 사람이 있으면
            # Fight!
            you_id = arr[ni][nj]
            yi,yj,yd,ys,ygun=player[you_id]

            me=ps+pgun
            you=ys+ygun # 공격력 비교

            if me>you or (me==you and ps>ys): win,lose=m,you_id  # 승패 인덱스
            elif me<you or (me==you and ps<ys): lose,win=m,you_id

            points[win]+=abs(me-you)

            # 패자 처리
            li, lj, ld, ls, lgun = player[lose]
            # 총 내려놓음
            if lgun==0:
                gun[ni][nj].append(lgun)

            # 방향 이동
            nni, nnj = li + dir[ld][0], lj + dir[ld][1]
            if not in_range(nni, nnj) or arr[nni][nnj]>0 : # out range or 다른 플레이어?
                while True: # 확인
                    ld=(ld+1)%4
                    nni, nnj = li + dir[ld][0], lj + dir[ld][1]
                    if in_range(nni, nnj) and arr[nni][nnj]==0:
                        break
                if len(gun[nni][nnj]) > 0:  # 총 없으니
                    lgun = max(gun[nni][nnj])  # 총 획득

                    gun[nni][nnj].remove(lgun)  # 가져간 건 지움

            player[lose]=nni,nnj,ld,ls,lgun
            arr[nni][nnj]=lose
            # print("패자 이동",nni,nnj)

            # 승자 처리
            wi, wj, wd, ws, wgun = player[win]
            # print("좌표 동일한지 비교", "이긴 플레이어", wi, wj, "싸운 칸", ni, nj)
            if len(gun[wi][wj])>0: # 총 있으면
                if wgun==0: # 플레이어 총 없으면
                    wgun=max(gun[wi][wj])# 총 획득
                    gun[wi][wj].remove(wgun) # 가져간 건 지움
                else: # 보유 총 이미 있으면
                    gun[wi][wj].append(wgun) # 내 총 먼저 내려놓고
                    wgun=max(gun[wi][wj]) # 가장 센 총 획득
                    gun[wi][wj].remove(wgun) # 가져간 건 지움
            player[win]=wi, wj, wd, ws, wgun  # 업데이트
            arr[wi][wj]=win

        else: # 사람이 없으면
            pi,pj=ni,nj
            arr[ni][nj]=m # 이동 => 뒤에서 해줘야 함
             # 총 확인
            if len(gun[ni][nj])>0: # 총 있으면
                if pgun==0: # 플레이어 총 없으면
                    pgun=max(gun[ni][nj]) # 총 획득
                    gun[ni][nj].remove(pgun) # 가져간 건 지움
                else: # 보유 총 이미 있으면
                    gun[ni][nj].append(pgun) # 내 총 먼저 내려놓고
                    pgun=max(gun[ni][nj]) # 가장 센 총 획득
                    gun[ni][nj].remove(pgun) # 가져간 건 지움
            player[m] = pi, pj, pd, ps, pgun  # 업데이트

print(*points[1:])