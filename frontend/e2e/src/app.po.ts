import { browser, by, element } from 'protractor';

export class AppPage {
  navigateTo() {
    return browser.get(browser.baseUrl) as Promise<any>;
  }

  navigateToPage(url: any) {
    return browser.get(url) as Promise<any>;
  }

  getTitleText() {
    return element(by.css('app-root .content span')).getText() as Promise<string>;
  }

  getCreateButton() {
    return element(by.xpath('/html/body/app-root/div[2]/app-view-games/div/div[1]/div[2]/a/button')).click() as Promise<any>;
  }

  getCreateGameHeading() {
    return element(by.className('login-title')).getText() as Promise<string>;
  }

  enterUsername() {
    return element(by.xpath('/html/body/app-root/div[2]/ng-component/div/div/div/form/div[1]/input')).sendKeys('Ben') as Promise<any>;
  }

  enterPassword() {
    return element(by.xpath('/html/body/app-root/div[2]/ng-component/div/div/div/form/div[2]/input')).sendKeys('test123') as Promise<any>;
  }

  clickLogin() {
    return element(by.xpath('/html/body/app-root/div[2]/ng-component/div/div/div/form/div[3]/button')).click() as Promise<any>;
  }
}
