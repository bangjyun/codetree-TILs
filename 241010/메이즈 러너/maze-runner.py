N, M, K=map(int,input().split())
arr=[list(map(int,input().split())) for _ in range(N)]
for _ in range(M):
    pi,pj=map(lambda x: int(x)-1,input().split())
    arr[pi][pj]-=1 # 사람-> arr에 표시

ei,ej=map(lambda x: int(x)-1,input().split()) # 이거 또 빼먹을뻔
arr[ei][ej]=-11 # 출구는 -11
p=0
def pprint(arr):
    print("\n".join(" ".join(f"{e:>3}" for e in l) for l in arr))

def in_range(i,j):
    return 0<=i<N and 0<=j<N

def rotate(arr,si,sj,L):
    narr=[x[:] for x in arr]
    for i in range(L):
        for j in range(L):
            narr[si+i][sj+j]=arr[si+L-1-j][sj+i]
            if narr[si+i][sj+j]>0:
                narr[si + i][sj + j]-=1
    return narr

def all_out():
    flag=0
    for pi in range(N):
        for pj in range(N):
            if -11<arr[pi][pj]<0: # 사람이 있으면
                flag=1
    if flag: return False
    else: return True

def exit_coord():
    flag=0
    for pi in range(N):
        for pj in range(N):
            if arr[pi][pj]==-11:
                return pi,pj
    return False # 오면 안 됨

tot_dist=0
#ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
for turn in range(K):
    blst=[] # 이동 전 좌표, 인원 수
    alst = []  # 이동 후 좌표, 인원 수
    flag = 0
    for pi in range(N):
        for pj in range(N):
            if -11 < arr[pi][pj] < 0:  # 사람이 있으면
                flag = 1
    if not flag: break
    if p: print(f"===================={turn}턴 시작=====================")
    if p: pprint(arr)

    # [1] 사람 이동
    for pi in range(N):
        for pj in range(N):
            if (pi,pj)==(ei,ej):
                continue
            if arr[pi][pj]<0: # 사람이라면
                for di,dj in ((-1,0),(1,0),(0,1),(0,-1)): # 상하좌우 확인
                    ni,nj=pi+di,pj+dj
                    if not in_range(ni,nj): continue
                    if arr[ni][nj]>0: continue# 벽이 있거나 격자 밖이면
                    if (ni, nj) == (ei, ej):
                        blst.append([pi, pj, arr[pi][pj]])
                        continue
                    if abs(ni-ei)+abs(nj-ej)< abs(pi-ei)+abs(pj-ej): # 지금보다 더 가까워진다면
                        # 이동 !
                        blst.append([pi,pj,arr[pi][pj]]) # 이동 전 좌표, 인원 수 -> 이만큼 없애야 함 +인원수
                        alst.append([ni, nj, arr[pi][pj]])  # 이동 전 좌표, 인원 수 (- 인원수)
                        break # 한 사람 이동 끝났으면 다른 방향 못 돌게 break

    if p: print("이동할 인원",blst)
    if p:print("이동후 인원", alst)
    # 동시에 이동
    for pi,pj,pnum in blst:
        arr[pi][pj]-=pnum # pnum은 (-인원수) -> 이만큼 빼줌
        tot_dist-=pnum
    for ai,aj,anum in alst:
        arr[ai][aj]+=anum # pnum은 (-인원수) -> 이만큼 빼줌

    if p: print(f"===================={turn}턴 사람 이동 후=====================")
    if p: pprint(arr)
    if turn==4:
        a = 1

    # [2] 미로 회전
    rlst=[]

    for L in range(2,N+1):
        for si in range(N-L+1):
            for sj in range(N-L+1):
                if si<=ei<si+L and sj<=ej<sj+L : # 출구가 있다면
                    for i in range(L):
                        for j in range(L):
                            if -11<arr[si+i][sj+j]<0: # 사람이 있으면
                                rlst.append([si,sj,L])
                                break

    if p: print("rotate 좌표, 길이",rlst,"출구",ei,ej)
    narr = [x[:] for x in arr]
    si,sj,L=rlst[0]
    narr = rotate(narr, si,sj,L) # 회전 후 내구도 감소
    arr = narr
    if p: print(f"===================={turn}턴 회전 후 =====================")
    if p: pprint(arr)
    ei, ej = exit_coord()

print(tot_dist)
print(ei+1,ej+1)