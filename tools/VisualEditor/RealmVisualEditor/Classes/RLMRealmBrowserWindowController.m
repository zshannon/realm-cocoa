////////////////////////////////////////////////////////////////////////////
//
// Copyright 2014 Realm Inc.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
// http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//
////////////////////////////////////////////////////////////////////////////

#import "RLMRealmBrowserWindowController.h"

#import "NSTableColumn+Resize.h"
#import "RLMNavigationStack.h"
#import "RLMApplicationDelegate.h"

const NSUInteger kMaxNumberOfArrayEntriesInToolTip = 5;

@implementation RLMRealmBrowserWindowController {

    RLMNavigationStack *navigationStack;
}

#pragma mark - NSViewController overrides

- (void)windowDidLoad
{
    navigationStack = [[RLMNavigationStack alloc] init];
    [self updateNavigationButtons];
    
    id firstItem = self.modelDocument.presentedRealm.topLevelClazzes.firstObject;
    if (firstItem != nil) {
        RLMNavigationState *initState = [[RLMNavigationState alloc] initWithSelectedType:firstItem
                                                                                   index:0];

        [self addNavigationState:initState
              fromViewController:nil];
    }
}

#pragma mark - Public methods - Accessors

- (RLMNavigationState *)currentState
{
    return navigationStack.currentState;
}

#pragma mark - Public methods

- (void)addNavigationState:(RLMNavigationState *)state fromViewController:(RLMViewController *)controller
{
    if (!controller.navigationFromHistory) {
        RLMNavigationState *oldState = navigationStack.currentState;
        
        [navigationStack pushState:state];
        [self updateNavigationButtons];
        
        if (controller == self.tableViewController || controller == nil) {
            [self.outlineViewController updateUsingState:state
                                                oldState:oldState];
        }
        
        [self.tableViewController updateUsingState:state
                                          oldState:oldState];
    }
}

- (IBAction)userClicksOnNavigationButtons:(NSSegmentedControl *)buttons
{
    RLMNavigationState *oldState = navigationStack.currentState;
    
    switch (buttons.selectedSegment) {
        case 0: { // Navigate backwards
            RLMNavigationState *state = [navigationStack navigateBackward];
            if (state != nil) {
                [self.outlineViewController updateUsingState:state
                                                       oldState:oldState];
                [self.tableViewController updateUsingState:state
                                                     oldState:oldState];
            }
            break;
        }
        case 1: { // Navigate backwards
            RLMNavigationState *state = [navigationStack navigateForward];
            if (state != nil) {
                [self.outlineViewController updateUsingState:state
                                                       oldState:oldState];
                [self.tableViewController updateUsingState:state
                                                     oldState:oldState];
            }
            break;
        }
        default:
            break;
    }
    
    [self updateNavigationButtons];    
}

#pragma mark - Private methods

- (void)updateNavigationButtons
{
    [self.navigationButtons setEnabled:[navigationStack canNavigateBackward]
                            forSegment:0];
    [self.navigationButtons setEnabled:[navigationStack canNavigateForward]
                            forSegment:1];
}

- (IBAction)insertObject:(id)sender
{
    
}

- (IBAction)removeObject:(id)sender
{

}

- (BOOL)validateMenuItem:(NSMenuItem *)menuItem
{
    RLMApplicationDelegate *applicationDelegate = (RLMApplicationDelegate *)[NSApplication sharedApplication].delegate;
    RLMNavigationState *currentState = self.currentState;
    
    if (menuItem == applicationDelegate.insertObjectMenuItem) {
        if ([currentState.selectedType isMemberOfClass:[RLMClazzNode class]]) {
            RLMClazzNode *clazzNode = (RLMClazzNode *)currentState.selectedType;
            return !clazzNode.hasChildNodes;
        }
    }
    else if (menuItem == applicationDelegate.removeObjectMenuItem) {
        if ([currentState.selectedType isMemberOfClass:[RLMClazzNode class]]) {
            RLMClazzNode *clazzNode = (RLMClazzNode *)currentState.selectedType;
            if (!clazzNode.hasChildNodes) {
                return currentState.selectedType.instanceCount > 0 && currentState.selectedInstanceIndex >= 0;
            }
        }
    }
    
    return NO;
}

@end
