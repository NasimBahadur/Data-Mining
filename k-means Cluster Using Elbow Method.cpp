/// In this program, I have just considered the integer part of all of my calculations for representation and calculation convenience.

#include<bits/stdc++.h>
using namespace std;

int distance(int x1,int y1,int x2,int y2)
{
    return pow(x1-x2,2)+pow(y1-y2,2);
}

int main()
{
    ///int t;
    ///cout<<"Enter the number of column or attribute of the dataset: ";
    ///cin>>t;
    ///int x[t],y[t],error[t/3],dist[t/3][2],cluster[t][2];
    ///for(int i=0; i<10; i++) cin>>x[i]>>y[i];

    int k=1, t=10, n=(t/3)+2, error[n], c[n][2], dist[n][t], cluster[t][2];
    int x[t]={1,7,2,0,9,3,5,8,6,4}, y[t]={2,0,1,8,1,6,0,0,7,3};
    cout<<"Points: ";
    for(int i=0; i<t; i++) cout<<"("<<x[i]<<","<<y[i]<<")"<<((i==t-1)?"\n":",");
    cout<<endl;

    while(k<=n)
    {
        int iteration=0,sum=0;
        for(int j=0; j<n; j++)
        {
            c[j][0]=x[j];
            c[j][1]=y[j];
        }
        cout<<((k>1)?"\n\n\n\n":"")<<"\t\t\t\t(For k = "<<k<<")"<<endl<<endl;

        while(iteration<100)
        {
            cout<<"Iteration-"<<iteration+1<<": "<<endl;
            for(int i=0; i<k; i++) cout<<"C"<<i+1<<" (old): "<<c[i][0]<<",  "<<c[i][1]<<endl;

            for(int j=0; j<k; j++)
            {
                cout<<"Distance-"<<j+1<<": ";
                for(int i=0; i<t; i++)
                {
                    dist[j][i]=distance(x[i],y[i],c[j][0],c[j][1]);
                    cout<<dist[j][i]<<((i==t-1)?"\n":",  ");
                    if(j>0)
                    {
                        if(cluster[i][0]>dist[j][i])  /// updated distance and cluster no. when recent distance is lesser than the previous one.
                        {
                            cluster[i][0]=dist[j][i];
                            cluster[i][1]=j;
                        }
                    }
                    else
                    {
                        cluster[i][0]=dist[j][i];  /// stored distance
                        cluster[i][1]=j;           /// stored cluster No.
                    }
                }
            }

            cout<<"Cluster: ";
            for(int i=0; i<t; i++) cout<<cluster[i][1]+1<<((i==t-1)?"\n":",  ");

            /// Error calculation (sse)
            for(int i=0; i<t; i++) sum+=cluster[i][0];
            cout<<"Error: "<<sum<<endl;

            /// Initialization with zero for storing new centroid
            for(int j=0; j<n; j++)
            {
                c[j][0]=0;
                c[j][1]=0;
            }
            /// Update centroid value
            for(int j=0; j<k; j++)
            {
                int k=0;
                for(int i=0; i<t; i++)
                {
                    if(cluster[i][1]==j)
                    {
                        c[j][0]+=x[i];
                        c[j][1]+=y[i];
                        k++;
                    }
                }
                c[j][0]/=k;
                c[j][1]/=k;
                cout<<"C"<<j+1<<" (new): "<<c[j][0]<<",  "<<c[j][1]<<endl;
            }

            /// When error value be same for more than once, iteration will stop
            if(error[k]==sum) break;
            error[k]=sum;
            sum=0;
            cout<<endl;
            iteration++;
        }
        k++;
    }

    cout<<"\n\n(K,Error): ";
    for(int i=1; i<=n; i++) cout<<"("<<i<<","<<error[i]<<")"<<((i==n)?"\n\n":",  ");
    cout<<"Slope: ";
    for(int i=1; i<=n; i++) cout<<error[i]/i<<((i==n)?"\n\n":",  ");

    return 0;
}
