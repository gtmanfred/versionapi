Vue.use(VueResource)
new Vue({
  el: '#app',
  data: {
    jobs: [],
  },
  methods: {
    submitJob: function(event) {
      let job = {
        "pr_num": this.$refs.pr_num.value.replace('#', ''),
        "commit_id": this.$refs.commit_id.value
      }
      event.preventDefault();
      this.$http.post("http://localhost/api/v1/tasks", job).then(function(response) {
        let job = response.data;
        job.ready = false;
        job.error = false;
        this.jobs.push(job);
        event.target.reset();
      });
    },
    getUrl: function (job) {
        if (job.result.rev.startsWith('#')) {
          return `https://github.com/${job.result.repo}/pull/${job.result.rev.replace('#', '')}`;
        } else {
          return `https://github.com/${job.result.repo}/commit/${job.result.rev}`;
        };
    },
    getReleaseNotes: function(job) {
      return `https://docs.saltstack.com/en/latest/topics/releases/${job.release.replace('v', '')}.html`;
    },
    isReady: function(job) {
      if (job.result && job.release) {
        return true;
      };
      return false;
    },
    checkJobs: function() {
      let newjobs = []
      while (this.jobs.length) {
        let job = this.jobs.pop()
        if (!job.result) {
          this.$http.get(`http://localhost/api/v1/tasks/${job.jid}`).then(function(response) {
            if (response.status == 200) {
              job['result'] = response.data.result;
              job.ready = true;
              if (job.result.tags) {
                job.release = job.result.tags[0];
              };
              if (job.release === undefined && job.result.branches) {
                this.$http.get(`http://localhost/api/v1/nextrelease/${job.result.repo}/${job.result.branches[0]}`).then(function(response){
                  job.release = `v${response.data.next}`;
                });
              };
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
