#include "cv.h"
#include "cvaux.h"
#include "highgui.h"

// for filelisting
#include <stdio.h>
#include <io.h>
// for fileoutput
#include <string>
#include <fstream>
#include <sstream>

using namespace std;

IplImage* image=0;
IplImage* image2=0;
int start_roi=0;
int roi_x0=0;
int roi_y0=0;
int roi_x1=0;
int roi_y1=0;
int numOfRec=0;
char* window_name="<SPACE>add <ENTER>save and load next <ESC>exit";

string IntToString(int num)
{
	ostringstream myStream; //creates an ostringstream object
	myStream << num << flush;
	/*
	* outputs the number into the string stream and then flushes
	* the buffer (makes sure the output is put into the stream)
	*/
	return(myStream.str()); //returns the string form of the stringstream object
};

void on_mouse(int event,int x,int y,int flag)
{
    if(event==CV_EVENT_LBUTTONDOWN)
    {
		start_roi=1;
		roi_x0=x;
		roi_y0=y;
    }
    if(event==CV_EVENT_MOUSEMOVE && flag==CV_EVENT_FLAG_LBUTTON)
    {
		roi_x1=x;
		roi_y1=y;

		//redraw ROI selection
		image2=cvCloneImage(image);
		cvRectangle(image2,cvPoint(roi_x0,roi_y0),cvPoint(roi_x1,roi_y1),CV_RGB(255,0,255),1);
		cvShowImage(window_name,image2);
		cvReleaseImage(&image2);
    }
    if(event==CV_EVENT_LBUTTONUP)
    {
		start_roi=0;
    }
}

int main(int argc, char** argv)
{

	struct _finddata_t bmp_file;
    long hFile;
	int iKey=0;
	
//	get *.bmp files in directory
	if((hFile=_findfirst("rawdata/*.bmp",&bmp_file))==-1L)
		printf("no *.bmp files in directory 'rawdata'\n");
	else
	{

	//	init highgui
		cvAddSearchPath("rawdata");
		cvNamedWindow(window_name,1);
		cvSetMouseCallback(window_name,on_mouse);

	//	init output of rectangles to the info file
		ofstream output("info.txt");

		string strPrefix;
		string strPostfix;

	//	open every *.bmp file
		do
		{
			printf(" %-12s\n",bmp_file.name);
			
			numOfRec=0;
			strPostfix="";
			strPrefix="rawdata/";
			strPrefix+=bmp_file.name;
			
			image=cvLoadImage(bmp_file.name,1);
			
		//	work on current image
			do
			{
				cvShowImage(window_name,image);
			
				// used cvWaitKey returns:
				//	<Enter>=13		save added rectangles and show next image
				//	<ESC>=27		exit program
				//	<Space>=32		add rectangle to current image
				//  any other key clears rectangle drawing only
				iKey=cvWaitKey(0);
				switch(iKey)
				{
				case 27:
						cvReleaseImage(&image);
						cvDestroyWindow(window_name);
						return 0;
				case 32:
						numOfRec++;
						// currently two draw directions possible:
						//		from top left to bottom right or vice versa
						if(roi_x0<roi_x1 && roi_y0<roi_y1)
						{
							printf("   %d. rect x=%d\ty=%d\twidth=%d\theight=%d\n",numOfRec,roi_x0,roi_y0,roi_x1-roi_x0,roi_y1-roi_y0);
							// append rectangle coord to previous line content
							strPostfix+=" "+IntToString(roi_x0)+" "+IntToString(roi_y0)+" "+IntToString(roi_x1-roi_x0)+" "+IntToString(roi_y1-roi_y0);
						}
						if(roi_x0>roi_x1 && roi_y0>roi_y1)
						{
							printf("   %d. rect x=%d\ty=%d\twidth=%d\theight=%d\n",numOfRec,roi_x1,roi_y1,roi_x0-roi_x1,roi_y0-roi_y1);
							// append rectangle coord to previous line content
							strPostfix+=" "+IntToString(roi_x1)+" "+IntToString(roi_y1)+" "+IntToString(roi_x0-roi_x1)+" "+IntToString(roi_y0-roi_y1);
						}
						break;
				}
			}
			while(iKey!=13);
			
			// save to info file as later used for HaarTraining:
			//	<rel_path>\bmp_file.name numOfRec x0 y0 width0 height0 x1 y1 width1 height1...
			if(numOfRec>0 && iKey==13)
			{
				//append line
				output << strPrefix << " "<< numOfRec << strPostfix <<"\n";
			}

			cvReleaseImage(&image);
		}
		while(_findnext(hFile,&bmp_file)==0);
		
		output.close();
		cvDestroyWindow(window_name);
		_findclose( hFile );
	}

	return 0;
}