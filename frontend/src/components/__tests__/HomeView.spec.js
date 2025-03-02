import { mount } from '@vue/test-utils';
import HomeView from '@/views/HomeView.vue';
import axios from 'axios';

// mock http requests
vi.mock('axios');

describe('HomeView.vue', () => {
  let wrapper;

  // creates a new instance of HomeView.vue
  beforeEach(() => {
    wrapper = mount(HomeView);
  });

  // removeFile test
  it('removeFile function test', async () => {
    // mock data for files and uploadedFiles array
    wrapper.setData(
      {
        files: [new File([], 'test_file.mp3')], 
        uploadedFiles: ['test_file.mp3']
      }
    );
    await wrapper.vm.$nextTick();

    // find the remove button and trigger it
    const removeButton = wrapper.find('button.btn-danger');
    await removeButton.trigger('click');
    
    // after the button is trigger, the length of files and uploadedFiles should be zero
    expect(wrapper.vm.files.length).toBe(0);
    expect(wrapper.vm.uploadedFiles.length).toBe(0);
  });

  it('performSearch with matches', async () => {
    // mock the backend response
    axios.get.mockResolvedValue({
      data: {
        data: [
          {
            filename: 'test_file.mp3', 
            transcribed_text: 'hello this is a unit test.'
          }
        ]
      }
    });
  
    // set the search query to 'unit'
    await wrapper.setData({searchQuery: 'unit'});
    await wrapper.vm.performSearch();

    // expect 1 record
    expect(wrapper.vm.dbRecords.length).toBe(1);
    expect(wrapper.vm.dbRecords[0].filename).toBe('test_file.mp3');
  });

  it('performSearch with no matches', async () => {
    // mock the backend response
    axios.get.mockResolvedValue({
      data: {
        data: []
      }
    });

    // set the search query to '|'
    await wrapper.setData({searchQuery: '|'});
    await wrapper.vm.performSearch();

    // expect 0 records
    expect(wrapper.vm.dbRecords.length).toBe(0);
  });
});
