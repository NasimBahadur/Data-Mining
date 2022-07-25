# Frequent Pattern Mining

In this Data Mining related work, A transactional dataset is used to mine the most frequent patterns of the purchased products using Apriori and Fp Growth algorithms. Moreover, the performance and comparison of memory usage and runtime between Apriori and Fp Growth algorithms are shown here. A hidden challenge in this work is to to work with real-life data and real-time performance analysis and comparison. 

<p align="center">
  <img src=https://user-images.githubusercontent.com/43060004/180801174-9785353d-25df-4921-b607-3e541d6818e4.png width="350" height="250"/>
  <img src=https://user-images.githubusercontent.com/43060004/180801191-47ead74a-7f84-4ef2-9577-46c82592acb7.png width="350" height="250"/>
</p>

The running time for certain dataset for a particular threshold should be too high that may not end in years. On the other hand for threshold on a particular dataset, there may not be any patterns available. So, choosing right threshold for each dataset is a challenge. In order to save time from waiting for outputs, I wrote a batch file for windows or a shell script for linux/mac where all the runs with required parameters or switches are listed. Once I ran the script or batch file from command line, I might set out for other works leaving my computer dealing with the computation by itself. Just we have to make sure no one turns computer off while the batch/script is running. All kinds of exception handling are included in the program. In case of an invalid switch or invalid value for a particular switch, program should show a helpful hint instead of treating the value in an inappropriate way or terminating abruptly.
