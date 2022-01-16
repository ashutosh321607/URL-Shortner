import { TestBed } from '@angular/core/testing';

import { HandleApiService } from './handle-api.service';

describe('HandleApiService', () => {
  let service: HandleApiService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(HandleApiService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
