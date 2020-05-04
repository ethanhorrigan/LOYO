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

  it('should open match page bb32763e7b6911ea95df02cd8b447e6d', () => {
    page.navigateToPage('/match/bb32763e7b6911ea95df02cd8b447e6d');
    expect(browser.getCurrentUrl()).toMatch('/match/bb32763e7b6911ea95df02cd8b447e6d');
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
    page.navigateToPage('/profile/Ben');
    expect(browser.getCurrentUrl()).toMatch('/profile/Ben');
  });

  //set up tests for registration
  //set up tests for login
  //set up tests for view games
  //set up tests for view match
  //set up tests for leaderboards

  afterEach(async () => {
    // Assert that there are no errors emitted from the browser
    const logs = await browser.manage().logs().get(logging.Type.BROWSER);
    expect(logs).not.toContain(jasmine.objectContaining({
      level: logging.Level.SEVERE,
    } as logging.Entry));
  });
});
