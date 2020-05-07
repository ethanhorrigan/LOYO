import { AppPage } from './app.po';
import { browser, logging } from 'protractor';

describe('workspace-project App', () => {
  let page: AppPage;

  beforeEach(() => {
    page = new AppPage();
  });

  // it('should display welcome message', () => {
  //   page.navigateTo();
  //   expect(page.getTitleText()).toEqual('frontend app is running!');

  // });

  it('should open display heading', () => {
    page.navigateToPage('/creategame');
    expect(page.getCreateGameHeading()).toEqual('Create a Game');
  });

  it('should open create page', () => {
    page.navigateToPage(browser.baseUrl);
    page.getCreateButton();
    expect(browser.getCurrentUrl()).toMatch('/creategame');
  });

  it('should open registration', () => {
    page.navigateToPage('/register');
    expect(browser.getCurrentUrl()).toMatch('/register');
  });

  it('should open login', () => {
    page.navigateToPage('/login');
    expect(browser.getCurrentUrl()).toMatch('/login');
  });

  it('should open view games', () => {
    page.navigateToPage('/viewgames');
    expect(browser.getCurrentUrl()).toMatch('/viewgames');
  });

  it('should open match page', () => {
    page.navigateToPage('/match/8e8c2fb2906d11eab67376772c75888d');
    expect(browser.getCurrentUrl()).toMatch('/match/8e8c2fb2906d11eab67376772c75888d');
  });

  it('should open leaderboards', () => {
    page.navigateToPage('/leaderboards');
    expect(browser.getCurrentUrl()).toMatch('/leaderboards');
  });

  it('should login a user', () => {
    page.navigateToPage('/login');
    page.enterUsername();
    page.enterPassword();
    page.clickLogin();
    page.navigateToPage('/mygames/Ben');
    expect(browser.getCurrentUrl()).toMatch('/mygames/Ben');
  });

  afterEach(async () => {
    // Assert that there are no errors emitted from the browser
    const logs = await browser.manage().logs().get(logging.Type.BROWSER);
    expect(logs).not.toContain(jasmine.objectContaining({
      level: logging.Level.SEVERE,
    } as logging.Entry));
  });
});
