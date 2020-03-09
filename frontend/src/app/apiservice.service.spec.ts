import { TestBed } from '@angular/core/testing';

import { APIServiceService } from './apiservice.service';
import { HttpClientTestingModule } from '@angular/common/http/testing';

describe('APIServiceService', () => {
  beforeEach(() => TestBed.configureTestingModule({  
    imports: [ HttpClientTestingModule ]
  }));

  it('should be created', () => {
    const service: APIServiceService = TestBed.get(APIServiceService);
    expect(service).toBeTruthy();
  });
});
