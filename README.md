# PaySlip Analysis (of Saama Technologies)
The project was created to automate the process of analyzing the trend of the salary and its breakdown by
   * Reading and parsing the PDFs
   * Generating a chronological CSV stating the following
       * Gross salary
       * Net salary
       * Deductions
   * Create a bar-plot and side-by-side graphs


# Docker
We need Python and Java (tabula-py) for reading parsing the PDFs. Slim versions of Debian Buster base images have been
used for a smaller footprint

* Upload the required files
   * Code
       * Dockerfile
       * requirements.txt
       * constants.py
       * environment.py
       * pay_slip_analysis.py
   * Salary slips to ./PDF directory

* Build an image
    * Use the following command to build an image
      * `docker build --no-cache=true --build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') --build-arg VCS_REF='asansari/payslip-analysis' --build-arg BUILD_VERSION='1.0' -t payslip-analysis:1.0 .`
    * The labels can be commented in the Dockerfile to reduce the number of layers

* Create and run within  a container
   * `docker run -it --rm --name payslip-analysis-container -v "$PWD":/usr/src/app -w /usr/src/app payslip-analysis:1.0`