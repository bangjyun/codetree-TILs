N,M,H,K=map(int,input().split())
runner=[]
arr=[[0]*N for _ in range(N)]
for i in range(M):
    x,y,d=map(int,input().split())
    runner.append((x-1,y-1,d))
    arr[x-1][y-1]=1

trees=set()
for i in range(H):
    x,y=map(int,input().split())
    trees.add((x-1,y-1))

dmap={1:(0,1),2:(1,0),3:(0,-1),4:(-1,0)} # 도망자 방향 맵
op={1:3,2:4,3:1,4:2}


# 방향  상 우 하 좌   tagger(술래)방향 (바깥으로 돌 때 방향)
tdi = [-1, 0, 1, 0]
tdj = [ 0, 1, 0,-1]

def pprint(arr):
    print("\n".join(" ".join(f"{elem:>3}" for elem in l) for l in  arr))


#ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
mx_cnt,cnt,flag,val=1,0,0,1
MM=N//2
ti,tj,td=MM,MM,0
tot_score=0
alive=[1]*M
for turn in range(1,K+1):
    # [1] 도망자 이동
    for m in range(M):
        if not alive[m]:
            continue
        ri,rj,rd=runner[m]
        if abs(ri-ti)+abs(rj-tj)<=3: # 거리가 3 이하인 도망자들만
            # 자기 방향으로 이동
            rdi, rdj = dmap[rd]
            ni, nj = ri + rdi, rj + rdj
            if 0<=ni<N and 0<=nj<N: # in range
                if (ni, nj) != (ti, tj):  # 술래 없으면
                    arr[ri][rj] -= 1  # 격자 이동처리
                    ri, rj = ni, nj  # 이동
                    arr[ni][nj] += 1
            # out range
            else:
                rd=op[rd] # 방향 바꿈
                rdi,rdj=dmap[rd]
                ni,nj=ri+rdi,rj+rdj
                if (ni,nj)!=(ti,tj): # 술래 없으면
                    arr[ri][rj] -= 1 # 격자 이동처리
                    ri,rj=ni,nj # 이동
                    arr[ni][nj]+=1

        runner[m]= ri,rj,rd # 업데이트

    # [2] 술래 이동
    # 이동 => 정답 참고함 -> 이건 암기하기
    cnt+=1
    ti,tj=ti+tdi[td],tj+tdj[td] # 이동 먼저
    if (ti, tj) == (0, 0):
        mx_cnt, cnt, flag, val = N, 1, 1, -1
        td=2
    if (ti,tj) == (MM, MM):
        mx_cnt, cnt, flag, val = 1, 0, 0, 1
        td=0
    else:
        if cnt == mx_cnt:
            cnt = 0
            td = (td + val)%4
            if flag:
                mx_cnt += val
                flag = 0
            else:
                flag = 1
    #
    # # 도망자 포획
    # ni,nj=ti,tj
    # for i in range(3): #
    #     if 0<=ni<N and 0<=nj<N and (ni,nj) not in trees:# 자료형이 틀려서 틀리다고 나올 수 있으니 확인 *
    #         rnum=arr[ni][nj]
    #         if rnum>0: # 나무가 없는데 도망자가 있으면
    #             tot_score+=turn*rnum
    #     for m in range(M):
    #         if not alive[m]:
    #             continue
    #         ri, rj, rd = runner[m]
    #         if (ri,rj)==(ni,nj): # 잡혔으면
    #             arr[ni][nj] = 0  # 도망자 제거
    #             alive[m]=0
    #     ni,nj=ni+tdi[td],nj+tdj[td]

    rnum=0
    ni, nj = ti, tj
    for i in range(3): #
        for m in range(M):
            ri, rj, rd = runner[m]
            if not alive[m]:
                continue
            if 0<=ni<N and 0<=nj<N and (ri,rj)==(ni,nj) and (ni,nj) not in trees:# 범위 내, 도망자 있고, 나무는 없을 떄
                rnum+=1
                alive[m] = 0
        ni, nj = ni + tdi[td], nj + tdj[td]
    tot_score += turn * rnum

print(tot_score)