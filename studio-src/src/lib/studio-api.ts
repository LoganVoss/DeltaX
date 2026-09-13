import type { MasteringModifiers, StyleId } from '@/lib/studio';

export interface StudioCommandApi {
  getState: () => Promise<unknown> | unknown;
  analyzeTrack: (signal?: AbortSignal) => Promise<unknown>;
  createTake: (input: {
    expectedStateVersion: number;
    baseStyle: StyleId;
    priorities: string[];
    constraints: string[];
    intensity?: number;
    modifiers?: MasteringModifiers;
    customName?: string;
    matchedDirections?: string[];
    creator: 'webmcp';
    prompt: string;
    signal?: AbortSignal;
  }) => Promise<unknown>;
  refineTake: (input: {
    expectedStateVersion: number;
    sourceTakeId: string;
    dimension: keyof MasteringModifiers;
    direction: 'increase' | 'decrease';
    amount: 'small' | 'medium';
    creator: 'webmcp';
    prompt: string;
    signal?: AbortSignal;
  }) => Promise<unknown>;
  createVariations: (input: {
    expectedStateVersion: number;
    styles: StyleId[];
    constraint:
      | 'preserve_transients'
      | 'keep_dynamic'
      | 'avoid_harshness'
      | 'none';
    creator: 'webmcp';
    prompt: string;
    signal?: AbortSignal;
  }) => Promise<unknown>;
  stageComparison: (input: {
    expectedStateVersion: number;
    takeIds: string[];
    creator: 'webmcp';
  }) => Promise<unknown>;
  setTrimFades: (input: {
    expectedStateVersion: number;
    startSeconds: number;
    endSeconds: number;
    fadeInSeconds: number;
    fadeOutSeconds: number;
    fadeInCurve?: number;
    fadeOutCurve?: number;
    creator: 'webmcp';
  }) => Promise<unknown>;
  setTrackSpeed: (input: {
    expectedStateVersion: number;
    speedPercent: number;
    creator: 'webmcp';
  }) => Promise<unknown>;
  commitMaster: (input: {
    expectedStateVersion: number;
    takeId: string;
    creator: 'webmcp';
  }) => Promise<unknown>;
}
