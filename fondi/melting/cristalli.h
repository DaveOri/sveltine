#include <Eigen/Core>
//#include <fstream>
#include <string>

using namespace std;
using namespace Eigen;

class crystal
{
   public:
	Vector3d CM;	//center of mass coordinate vector

	long int N;		//number of dipoles

	MatrixX4d dipoles;	//array of dipoles coordinates Nx4

	double d;		//interdipole spacing in micrometers
	double Dmax;		//maximum dimension!!
	
	crystal();			// !!! VUOTO  !!!

//	static crystal column(double,double);
//	static crystal spheroid(double,double,double);
	static crystal load_round(string);

//	void rotate(double,double,double,double);	// x y z rotation
//	void rotate();								// x y z random rotation
//	void translate(double,double,double);// x y z traslation

//	void addColumn(double);	// d deve essere quello dell'oggetto, dunque non serve

	crystal rounder();

	void save(string);
	void saveDDSCAT6_1(string);
};
