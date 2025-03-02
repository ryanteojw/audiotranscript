<template>
  <div class="container-fluid">
    <!-- upload audio file section -->
    <div class="row mb-4">
      <div class="col-12">
        <div>
          <h1 class="mt-1">Upload Audio File</h1>
          <div>
            <!-- file input -->
            <div class="row">
              <div class="col-8">
                <input 
                  type="file" 
                  @change="handleFileUpload" 
                  multiple 
                  class="file-input form-control" 
                  ref="fileInput"
                />
              </div>
              <!-- button to upload the files -->
              <div class="col-4">
                <button @click="uploadFiles" class="btn btn-primary w-25" :disabled="isUploadLoading">
                  <!-- loading circle -->
                  <span v-if="isUploadLoading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                  <span v-else>Upload Files</span>
                </button>
              </div>
            </div>
          </div>
          <!-- display uploaded files -->
          <div v-if="uploadedFiles.length > 0" class="mt-3">
            <h3>Selected Files:</h3>
            <ul class="p-0 m-0">
              <li v-for="(filename, index) in uploadedFiles" :key="index" class="mb-2 p-2 border rounded bg-light d-flex justify-content-between align-items-center">
                {{ filename }}
                <!-- include a button to remove the uploaded files if the user wish to -->
                <button @click="removeFile(index)" class="btn btn-danger btn-sm">Remove</button>
              </li>
            </ul>
          </div>
          <!-- success message -->
          <div v-else-if="isUploadedSuccessful" class="border border-success rounded p-3 text-white mt-3" style="background-color: #4CAF50;">
            Successfully uploaded all files!
          </div>
          <!-- files that failed to upload -->
          <div v-else-if="failedFiles.length > 0" class="border border-danger rounded p-3 text-white mt-3" style="background-color: #dc3545;">
            <h3>Failed to upload {{ failedFiles.length }} file{{ failedFiles.length > 1 ? 's' : '' }}:</h3>
            <ul class="p-0 m-0">
              <li v-for="filename in failedFiles" class="list-group-item list-group-item-danger mb-2 p-2 rounded border border-danger">
                {{ filename }}
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <!-- audio records table section -->
    <div class="row">
      <div class="col-12">
        <div>
          <h1 class="mt-1">Audio Records</h1>
          <!-- search field -->
          <div class="row mb-3">
            <div class="col-8">
              <input 
                type="text" 
                v-model="searchQuery" 
                placeholder="Search by filename or transcribed text" 
                class="form-control"
                @keydown.enter="performSearch"
              />
            </div>
            <div class="col-4">
              <!-- search button -->
              <button @click="performSearch" class="btn btn-primary" :disabled="isSearchLoading">
                  <!-- loading circle -->
                  <span v-if="isSearchLoading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                  <span v-else>Search</span>
              </button>
              <!-- display all transcriptions button -->
              <button @click="fetchData" class="btn btn-secondary" :disabled="isSearchLoading" style="margin-left: 15px;">
                  <!-- loading circle -->
                  <span v-if="isDisplayAllLoading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                  <span v-else>Display All</span>
              </button>
            </div>
          </div>
          <!-- audio data table -->
          <div class="table-responsive mb-3" style="max-height: 475px; overflow-y: auto;">
            <table v-if="dbRecords.length > 0" class="table table-striped table-bordered">
              <thead class="text-center">
                <tr>
                  <th class="py-3" style="width: 15%;">Filename</th>
                  <th class="py-3" style="width: 20%;">Audio</th>
                  <th class="py-3" style="width: 50%;">Transcribed Text</th>
                  <th class="py-3" style="width: 15%;">Uploaded Timestamp</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(record, index) in dbRecords" :key="index">
                  <td class="border text-center">{{ record.filename }}</td>
                  <td class="border text-center">
                    <!-- display the audio file -->
                    <audio :src="record.file_data" controls></audio>
                  </td>
                  <td class="border text-center">{{ record.transcribed_text }}</td>
                  <td class="border text-center">{{ record.uploaded_timestamp ? record.uploaded_timestamp.slice(5, 16) + " " + record.uploaded_timestamp.slice(17, 25) : ""}}</td>
                </tr>
              </tbody>
            </table>
            <p v-else class="no-records">No audio records found!</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { getAllTranscriptions, createAudioTranscribe, getFilteredAudioData } from "@/api/apiService.js";

export default {
  data() {
    return {
      files: [],
      uploadedFiles: [],
      failedFiles: [],
      dbRecords: [],
      searchQuery: "",
      isDisplayAllLoading: false,
      isUploadLoading: false,
      isSearchLoading: false,
      isUploadedSuccessful: false
    }
  },
  methods: {
    async fetchData() {
      try {
        this.isDisplayAllLoading = true;
        // async call to the backend API to get all transcriptions in the db
        const response = await fetch(getAllTranscriptions);
        const data = await response.json();
        this.dbRecords = data.data; 
        console.log(this.dbRecords[0].uploaded_timestamp);
      } catch (error) {
        console.error("error fetching data:", error);
      }
      finally {
        this.isDisplayAllLoading = false;
      }
    },
    handleFileUpload(event) {
      // set all the previous variables to its original value
      this.isUploadedSuccessful = false;
      this.uploadedFiles = [];
      this.failedFiles = [];
      this.allFilesFailed = false;
      
      // convert FileList into an array to be used in removeFile function
      this.files = [];
      for (let i = 0; i < event.target.files.length; i++) {
        this.files.push(event.target.files[i]);
      }
      console.log(this.files);
      // loop to update the uploadedFiles array to show the users on the files to be uploaded
      for (let i = 0; i < this.files.length; i++) {
        let file_name = this.files[i].name;
        this.uploadedFiles.push(file_name);
      }
      console.log(this.uploadedFiles);
    },
    removeFile(index) {
      // to remove from exisitng lists to show the files to be uploaded
      this.uploadedFiles.splice(index, 1);
      this.files.splice(index, 1);

      // update text displayed next to choose files button
      if (typeof DataTransfer !== 'undefined') {
        const dataTransfer = new DataTransfer();
        this.files.forEach(file => dataTransfer.items.add(file));
        this.$refs.fileInput.files = dataTransfer.files;
      }
    },
    async uploadFiles() {
      this.isUploadLoading = true;
      console.log(this.files);
      // if there is not files to be uploaded then the function stops
      if (this.files.length === 0) {
        this.isUploadLoading = false;
        return;
      }

      // create FormData obj to send to backend
      const formData = new FormData();
      for (let i = 0; i < this.files.length; i++) {
        formData.append('audioFiles', this.files[i]);
      }
  
      try {
        console.log(formData);
        this.isUploadedSuccessful = false;
        const response = await axios.post(createAudioTranscribe, formData);
        console.log(response);
        // success response
        if (response.status === 200) {
          this.isUploadedSuccessful = true;
        }
      }
      catch (error) {
        // error response
        for (let i = 0; i < error.response.data.data.length; i++) {
          this.failedFiles.push(error.response.data.data[i]);
        }
        console.log(error);
      }
      finally {
        this.fetchData();
        this.isUploadLoading = false;
        this.uploadedFiles = [];
        this.files = [];
      }
    },
    async performSearch() {
      console.log(this.searchQuery);
      this.isSearchLoading = true;

      try {
        // call the search api
        const response = await axios.get(`${getFilteredAudioData}?query=${this.searchQuery}`);
        console.log(response);
        // update dbRecords
        this.dbRecords = response.data.data;
      } catch (error) {
        console.error('error fetching data:', error);
      } finally {
        this.isSearchLoading = false;
      }
    },
  },
  mounted() {
    this.fetchData();
  }
};
</script>
