L,N,Q=map(int,input().split())
arr= [[2]*(L+2)]+[[2]+list(map(int,input().split()))+[2] for _ in range(L)]+[[2]*(L+2)]
bomb = set()
for i in range(L+2):
    for j in range(L+2):
        if arr[i][j]==1: # 함정
            bomb.add((i,j))
            arr[i][j]=0
out=[0]*(N+1)
knight={}
for m in range(1,N+1):
    r,c,h,w,k=map(int,input().split())
    knight[m]=[r,c,h,w,k,0] # x,y,max_dx,max_dy(좌표 더하면 끝 좌표), 체력, dmg 입은 것
    for i in range(r, r + h):
        for j in range(c, c + w):
            arr[i][j] = -m  # 체스판에 -idx 표시

Qlst=[list(map(int,input().split())) for _ in range(Q)]
qdi=[-1,0,1,0]
qdj=[0,1,0,-1]

def pprint(arr):
    print("\n".join(" ".join(f"{e:>3}" for e in l) for l in arr))

from collections import deque
def move_knight(idx):
    q=deque([idx])
    global fset # 이동할 기사들의 인덱스 저장 set
    fset.add(idx)

    while q: # 나 이동 가능? & 나 말고 다른 애들도 이동 가능?
        cidx=q.popleft()
        ci, cj, ch, cw, ck, cdmg = knight[cidx]
        for i in range(ci, ci + ch):
            for j in range(cj, cj + cw):  # 현재 기사의 바운더리 통째로 qd 이동 -> 원소 중에 2 있으면 먼저 break, 다른 기사 있으면 nq에 append
                ni, nj = i + qdi[qd], j + qdj[qd] # 지금 뽑힌 애가 이동 가능한지를 확인
                if arr[ni][nj] == 2:  # 벽
                    fset=set() # 사실 의미 없음
                    return False
                elif -31< arr[ni][nj]<0 and arr[ni][nj]!=arr[ci][cj] : # 다른 기사가 있는 경우 (나 말고)
                    nidx= - arr[ni][nj]
                    if out[nidx]: continue  # 그 인덱스 없어!
                    q.append(nidx)
                    fset.add(nidx)
    return True


for qi,qd in Qlst: # 명령받은 기사 인덱스, 방향
    fset=set()
    # print(f"============={qi,qd}==========")
    if out[qi]: continue # 그 인덱스 없어!
    if len(knight)==0: # 기사 전멸
        break

    narr=[x[:] for x in arr]
    if move_knight(qi): # 이동 시작 (이동 가능하니 벽은 상관 X)
        for fidx in fset:  # 해당하는 기사들
            fi, fj, fh, fw, fk, fdmg = knight[fidx]
            for i in range(fi, fi + fh):
                for j in range(fj, fj + fw):  # 동시에 이동
                    ni, nj = i + qdi[qd], j + qdj[qd]  # 이동
                    narr[i][j] -= arr[i][j]
                    narr[ni][nj] += arr[i][j]
                    if (ni, nj) in bomb and fidx != qi:  # 함정이 있으면, !!!!! 놓침: 명령받은 기사는 피해를 입지 않는다
                        fdmg += 1
                        fk -= 1
            fi, fj = fi + qdi[qd], fj + qdj[qd]  # 좌상단 좌표 업데이트
            knight[fidx] = fi, fj, fh, fw, fk, fdmg  # 업데이트
        arr = narr

        for fidx in fset:  # 해당하는 기사들
            fi, fj, fh, fw, fk, fdmg = knight[fidx]
            if fk<=0: # 체력 바닥남
                out[fidx]=1
                knight.pop(fidx) # 삭제해버리기
                for i in range(fi, fi + fh):
                    for j in range(fj, fj + fw):
                        arr[i][j]=0

tot_dmg=0
for live_knight in knight.values():
    tot_dmg+=live_knight[5]
print(tot_dmg)