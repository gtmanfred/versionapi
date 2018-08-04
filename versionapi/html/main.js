Vue.use(VueResource)
new Vue({
  el: '#app',
  data: {
    jobs: [],
  },
  methods: {
    submitJob: function(event) {
      let job = {
        "pr_num": this.$refs.pr_num.value,
        "commit_id": this.$refs.commit_id.value
      }
      event.preventDefault();
      this.$http.post("http://localhost:5000/api/v1/tasks", job).then(function(response) {
        let job = response.data;
        job.ready = false;
        job.error = false;
        this.jobs.push(job);
        event.target.reset();
      });
    },
    checkJobs: function() {
      let newjobs = []
      while (this.jobs.length) {
        let job = this.jobs.pop()
        if (!job.result) {
          this.$http.get(`http://localhost:5000/api/v1/tasks/${job.jid}`).then(function(response) {
            if (response.status == 200) {
              job['result'] = response.data.result;
              job.ready = true;
              if (job.result.error) {
                job.error = true;
              }
            };
          });
        };
        newjobs.push(job)
      };
      this.jobs = newjobs.reverse();
    }
  },
  mounted: function () {
    setInterval(this.checkJobs, 5000); 
  }
});
