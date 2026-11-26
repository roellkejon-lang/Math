#include <stdio.h>
#include <stdlib.h>
/* wires: 0..2 left x_u, 3..7 right y_v; value = 15-bit mask over (u,v), bit 5u+v */
static int W[32], A[32], B[32], O[32], n0=8, maxg, target, found=0;
static long nodes=0;
static void print(int g){ for(int j=0;j<g;j++) printf("gate %d (wire %d) = %s(w%d, w%d)  mask=%d\n", j, n0+j, O[j]?"OR":"AND", A[j], B[j], W[n0+j]); }
static void dfs(int g){
  nodes++;
  if (g==maxg) return;
  int w=n0+g;
  for(int a=0;a<w;a++) for(int b=a+1;b<w;b++) for(int op=0;op<2;op++){
    if (g>0){ int pw=w-1; if (a!=pw && b!=pw){ /* previous gate not read: enforce order */
      int pa=A[g-1],pb=B[g-1],po=O[g-1];
      if (a<pa || (a==pa && (b<pb || (b==pb && op<=po)))) continue; } }
    int v = op ? (W[a]|W[b]) : (W[a]&W[b]);
    int dup=0; for(int k=0;k<w;k++) if(W[k]==v){dup=1;break;} if(dup) continue;
    if (v==0 || v==0x7fff) continue;
    W[w]=v; A[g]=a; B[g]=b; O[g]=op;
    if (v==target){ printf("FOUND with %d gates\n", g+1); print(g+1); found=1; exit(0); }
    dfs(g+1);
  }
}
int main(int c,char**v){ target=atoi(v[1]); maxg=atoi(v[2]);
  for(int u=0;u<3;u++){int m=0; for(int j=0;j<5;j++) m|=1<<(5*u+j); W[u]=m;}
  for(int j=0;j<5;j++){int m=0; for(int u=0;u<3;u++) m|=1<<(5*u+j); W[3+j]=m;}
  int lim=maxg; for(int g=1; g<=lim && !found; g++){ maxg=g; dfs(0); fprintf(stderr,"no circuit with %d gates (nodes %ld)\n", g, nodes); }
  maxg=atoi(v[2]); return 0; }
