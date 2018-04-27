#include <boost/program_options.hpp>
#include <iostream>

#include "argument_parser.h"

using namespace std;
namespace po = boost::program_options;

argument_parser::argument_parser(int argn, char** argv){
	po::options_description description("Allowed options");
	
	cout<<"Parser created with "<<argn<<" arguments"<<endl;
	description.add_options()
		("help", "produce help message")
		("options", "list options")
		("melt",po::value<double>(),"set wanted melting fraction")
		("dipole",po::value<double>(),"set interdipole spacing")
		("dmax",po::value<double>(),"set particle maximum dimension for header comment")
		("input",po::value<string>(),"set input file name")
		("output",po::value<string>(),"set output file name")
	;

	po::store(po::parse_command_line(argn, argv, description), vm);
	po::notify(vm);

	if (vm.count("help")) {
		cout<<"This is the theta program, please type --options for list of available options"<<endl;
	}

	if (vm.count("options")) {
		cout<<description<<endl;
	}

	if (vm.count("melt")) {
		cout<<"requested melted fraction is "<<vm["melt"].as<double>()<<endl;
	} else {
		cout<<"no melting fraction requested"<<endl;
		exit(0);
	}
	
	if (vm.count("dipole")) {
		cout<<"passed interdipole spacing is "<<vm["dipole"].as<double>()<<endl;
	} else {
		cout<<"no interdipole spacing passed"<<endl;
		exit(0);
	}

	if (vm.count("dmax")) {
		cout<<"passed maximum dimension is "<<vm["dmax"].as<double>()<<endl;
	} else {
		cout<<"no maximum dimension passed"<<endl;
		exit(0);
	}
	
	if (vm.count("input")) {
		cout<<"input filename is is "<<vm["input"].as<string>()<<endl;
	} else {
		cout<<"no input filename passed "<<endl;
		exit(0);
	}

	if (vm.count("output")) {
		cout<<"output filename is is "<<vm["output"].as<string>()<<endl;
	} else {
		cout<<"no output filename passed "<<endl;
		exit(0);
	}
};
