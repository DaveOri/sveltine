#include "cristalli.h"
//#include <string> //già incluso in cristalli.h
#include <iostream>
#include <sstream>
#include <omp.h>
#include <math.h>
#include <stdlib.h>
#include <time.h>

#include <boost/random/mersenne_twister.hpp>
#include <boost/random/uniform_real_distribution.hpp>
using namespace boost::random;
//using namespace std; //già incluso in cristalli.h

int main()
{
	srand(time(NULL));
	double d=20;
	crystal aggregato=crystal::load_round("./mix1Col1026.64.dat");
	aggregato.Dmax=1026.64;
	double f=60./100.;
	unsigned long int Nwater=round(aggregato.N*f);
	cout<<"Nwater   "<<Nwater<<endl;
	unsigned long int melted=0;
	int I,J,K;
//	unsigned long int melting_idx=0;
// trovare i limiti estremi della particella e aggiungere o togliere 1 /// FATTO	
	int Xmin=0,Xmax=0,Ymin=0,Ymax=0,Zmin=0,Zmax=0;
	for(int i=0;i<aggregato.N;i++)
	{
		Xmax=aggregato.dipoles(i,0)>Xmax?(int)aggregato.dipoles(i,0):Xmax;
		Ymax=aggregato.dipoles(i,1)>Ymax?(int)aggregato.dipoles(i,1):Ymax;
		Zmax=aggregato.dipoles(i,2)>Zmax?(int)aggregato.dipoles(i,2):Zmax;
		Xmin=aggregato.dipoles(i,0)<Xmin?(int)aggregato.dipoles(i,0):Xmin;
		Ymin=aggregato.dipoles(i,1)<Ymin?(int)aggregato.dipoles(i,1):Ymin;
		Zmin=aggregato.dipoles(i,2)<Zmin?(int)aggregato.dipoles(i,2):Zmin;
	}
	Xmax++;
	Ymax++;
	Zmax++;
	Xmin--;
	Ymin--;
	Zmin--;

//	posizionare i dipoli in un array tridimensionale di interi con possibili stati
// 0 aria
// 1 ghiaccio
// 2 acqua
	int Xdim=Xmax-Xmin+1;
	int Ydim=Ymax-Ymin+1;
	int Zdim=Zmax-Zmin+1;
	int lattice[Xdim][Ydim][Zdim];
	for(int i=0;i<Xdim;i++)
	{
		for(int j=0;j<Ydim;j++)
		{
			for(int k=0;k<Zdim;k++)
			{
				lattice[i][j][k]=0; // metto tutto ad aria
			}
		}
	}
	for(int i=0;i<aggregato.N;i++)
	{
		lattice[(int)aggregato.dipoles(i,0)-Xmin+1][(int)aggregato.dipoles(i,1)-Ymin+1][(int)aggregato.dipoles(i,2)-Zmin+1]=aggregato.dipoles(i,3); //saranno tutte 1
	}
	mt19937_64 gen;
	gen.seed(time(NULL));
	uniform_real_distribution<double> uniform(0.,1.); //la dichiaro una volta poi la moltiplico per la cdf dell'ultimo elemento
	double meltprob[Xdim*Ydim*Zdim];
	unsigned long int index;
	double probability;
	double probair=1.;
	double probwat=0.1;
	double probice=0.;

	while(melted<Nwater)
	{
		index=0;
		meltprob[0]=0.;//facendo parte del contorno è aria
		for(int i=0;i<Xdim;i++)
		{
			for(int j=0;j<Ydim;j++)
			{
				for(int k=0;k<Zdim;k++) //il primo l'ho fatto a parte // aspetta, se parto da k=1 ne salto uno a ogni giro di j
				{
					if(i+j+k)	//il primo l'ho fatto a parte altrimenti non funziona... forse si può trovare un modo migliore invece che chiamare un if a ogni ciclo
					{
						index++;
						meltprob[index]=meltprob[index-1];
						if(lattice[i][j][k]) //lo faccio solo se non è aria, così escludo il contorno che da problemi di out of bounds
						{
							if(lattice[i][j][k]!=2)  //lo faccio solo se non è già fuso
							{
								switch(lattice[i][j][k+1])
								{
									case 0: meltprob[index]+=probair;
									case 1: meltprob[index]+=probice;
									case 2: meltprob[index]+=probwat;
								} 								
								switch(lattice[i][j][k-1])
								{
									case 0: meltprob[index]+=probair;
									case 1: meltprob[index]+=probice;
									case 2: meltprob[index]+=probwat;
								} 								
								switch(lattice[i][j+1][k])
								{
									case 0: meltprob[index]+=probair;
									case 1: meltprob[index]+=probice;
									case 2: meltprob[index]+=probwat;
								} 								
								switch(lattice[i][j-1][k])
								{
									case 0: meltprob[index]+=probair;
									case 1: meltprob[index]+=probice;
									case 2: meltprob[index]+=probwat;
								} 								
								switch(lattice[i+1][j][k])
								{
									case 0: meltprob[index]+=probair;
									case 1: meltprob[index]+=probice;
									case 2: meltprob[index]+=probwat;
								} 								
								switch(lattice[i-1][j][k])
								{
									case 0: meltprob[index]+=probair;
									case 1: meltprob[index]+=probice;
									case 2: meltprob[index]+=probwat;
								} 								
							}
						}
					}				
				}
			}
		}
		cout<<"index "<<index<<" cumprob "<<meltprob[index];
		probability=meltprob[index]*uniform(gen);
		cout<<"  prob"<<probability<<"  ";
		index=0;
		while(meltprob[index]<probability)
		{
			index++;
		}
		cout<<index<<" ";
		I=(int)floor(((double)index)/((double)(Zdim*Ydim)));
		J=(int)floor(((double)(index-I*Zdim*Ydim))/((double)(Zdim)));
		K=index-I*Ydim*Zdim-J*Zdim;
		cout<<" prima "<<lattice[I][J][K]<<" ";
		lattice[I][J][K]=2; // fuuuuu-sio'......NEEEEEEEEEEEEE!!!!!!!!!!!!!!!!
		cout<<" dopo "<<lattice[I][J][K]<<" ";
		cout<<"IJK "<<I<<" "<<J<<" "<<K<<endl;
		cout<<"XYZ "<<I+Xmin-1<<" "<<J+Ymin-1<<" "<<K+Zmin-1<<endl;
		melted++;
	}
// riconvertire l'array tridimensionale in crystal
	for(int i=0;i<aggregato.N;i++)
	{
		aggregato.dipoles(i,3)=lattice[(int)aggregato.dipoles(i,0)-Xmin+1][(int)aggregato.dipoles(i,1)-Ymin+1][(int)aggregato.dipoles(i,2)-Zmin+1];
	}
// salvare la particella
	string MR="MR";
	string Col="Col";
	ostringstream oss;
	oss<<f*100.;
	string fraction=oss.str();
	MR.append(fraction);
	MR.append(Col);
	aggregato.saveDDSCAT6_1(MR);
}
