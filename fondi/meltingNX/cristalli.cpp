#include "cristalli.h"
#include <math.h>
#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <stdlib.h>
#include <time.h>

//using namespace std;
//using namespace Eigen;

crystal::crystal(){};

crystal crystal::rounder()
{
	crystal rounded;
	rounded.N=N;
	rounded.d=d;
	rounded.Dmax=Dmax;
	rounded.CM=CM;
	rounded.dipoles.resize(N,4);
	long int copied=0;
	bool superposition=false;
	RowVector4d temp;

	for(long int i=0;i<N;i++)
	{
		temp(0)=round(dipoles(i,0));
		temp(1)=round(dipoles(i,1));
		temp(2)=round(dipoles(i,2));
		temp(3)=dipoles(i,3);
		for(long int j=0;j<copied;j++)
		{
			if(temp==rounded.dipoles.row(j))
			{
				superposition=true;
			}
		}
		if(!superposition)
		{
			rounded.dipoles.row(copied)=temp;
			copied++;
		}
		superposition=false;
	}
	// eventualmente rimetto a posto il CM???
	rounded.dipoles.conservativeResize(copied,4);
	rounded.N=copied;
	return rounded;
};

void crystal::save(string LABEL)
{
	ostringstream oss;
	oss<<Dmax;
	string MaximumDimension = oss.str();
	string extension(".dat");
	LABEL.append(MaximumDimension);
	LABEL.append(extension);
	ofstream OUT(LABEL.c_str());
	OUT<<dipoles;
	OUT.close();
};

void crystal::saveDDSCAT6_1(string LABEL)
{
	ostringstream oss;
	oss<<Dmax;
	string MaximumDimension = oss.str();
	string extension(".dat");
	LABEL.append(MaximumDimension);
	LABEL.append(extension);
	ofstream OUT(LABEL.c_str());
	double aeff=d*pow(0.25*3*N/M_PI,1./3.);//
	OUT<<"Aggregate with Dmax= "<<Dmax<<" and aeff= "<<aeff<<endl;
	OUT<<N<<"  = NAT"<<endl;
	OUT<<"1.000\t0.000\t0.000\t= target vector a1 (in TF)"<<endl;
	OUT<<"0.000\t1.000\t0.000\t= target vector a1 (in TF)"<<endl;
	OUT<<"1.\t1.\t1.\t= d_x/d d_y/d d_z/d (normally 1 1 1)"<<endl;
	OUT<<"J\tJX\tJY\tJZ\tICMPX\tICMPY\tICMPZ"<<endl;
	MatrixX2d IDX_COMP;
	IDX_COMP.resize(N,2);
	for(int i=0; i<N; i++)
	{
		IDX_COMP(i,0)=dipoles(i,3);
		IDX_COMP(i,1)=dipoles(i,3);
	}
	VectorXd n;
	n=VectorXd::LinSpaced(N,1,N);
	MatrixXd n_dipoles_ICOMP(N,7);
	n_dipoles_ICOMP<<n,dipoles,IDX_COMP;
	OUT<<n_dipoles_ICOMP;
	OUT.close();
};

crystal crystal::load_round(string previous)
{
	crystal temp;

	ifstream IN;
	const char *name;
   name = previous.c_str();
	IN.open(name, std::ifstream::in);
	IN.seekg (0, ios::end);
	int caratteri = IN.tellg();
	IN.seekg (0, ios::beg);
	cout<<caratteri<<endl;

	char* buffer;
	buffer=new char[caratteri];
	IN.read(buffer,caratteri);
	std::cout<<"leggo il buffer   ";
	int righe=0;
	for (int i=0; i<caratteri; i++) 
	{
		if(buffer[i]==0x0A) //carattere di mandata a capo
		{
			righe++;
		}
	}
	cout<<"Il nostro file è lungo "<<++righe<<" righe"<<endl; //perchè il file è terminato con un eof invece che con un endl, quindi ne conta una in meno
	temp.N=righe;
	temp.dipoles.resize(righe,4);
	cout<<"Ho creato i vettori"<<endl;
	IN.seekg (0, ios::beg);
	cout<<"Mi sono rimesso all'inizio"<<endl;
	for(int i=0;i<righe;i++)
	{
		IN>>temp.dipoles(i,0)>>temp.dipoles(i,1)>>temp.dipoles(i,2);
		temp.dipoles(i,3)=1;
	}
	std::cout<<"Ho riempito i vettori"<<std::endl;
	return temp.rounder();	
}

crystal crystal::load_R(string previous)
{
	crystal temp;

	ifstream IN;
	const char *name;
   name = previous.c_str();
	IN.open(name, std::ifstream::in);
	IN.seekg (0, ios::end);
	int caratteri = IN.tellg();
	IN.seekg (0, ios::beg);
	cout<<caratteri<<endl;

	char* buffer;
	buffer=new char[caratteri];
	IN.read(buffer,caratteri);
	std::cout<<"leggo il buffer   ";
	int righe=0;
	for (int i=0; i<caratteri; i++) 
	{
		if(buffer[i]==0x0A) //carattere di mandata a capo
		{
			righe++;
		}
	}
	cout<<"Il nostro file è lungo "<<++righe<<" righe"<<endl; //perchè il file è terminato con un eof invece che con un endl, quindi ne conta una in meno
	temp.N=righe-6;   // ci sono 6 righe di header
	temp.dipoles.resize(temp.N,4);
	cout<<"Ho creato vettori   "<<temp.N<<endl;
	IN.seekg (0, ios::beg);
	cout<<"Mi sono rimesso all'inizio"<<endl;
	
	righe=0;
	int equals=0;
	int useless;
	char c;
	double aeff;
	while(righe<6)
	{
		c=IN.get();
		if(c==0x3D)
		{
			equals++;
			if(equals==2)
			{
				IN>>aeff;
				cout<<"Ho letto aeff  "<<aeff<<endl;
			}
		}
		if(c==0x0A)
		{
			righe++;
		}
	}
	cout<<"Mi sono posizionato all'inizio della settima riga"<<endl;
	for(int i=0;i<temp.N;i++)
	{
		IN>>useless>>temp.dipoles(i,0)>>temp.dipoles(i,1)>>temp.dipoles(i,2)>>useless>>useless>>useless;
		temp.dipoles(i,3)=1;
	}
	std::cout<<"Ho riempito i vettori"<<std::endl;
	temp.d=aeff*pow((4.*M_PI)/(temp.N*3.),1./3.);
	cout<<"Ho calcolato d   "<<temp.d<<endl;
	return temp;	
}
