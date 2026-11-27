export interface Course {
  id: number;
  courseCode: string;
  title: string;
  credits: number;
}

export interface CourseDetails extends Course {
  description: string | null;
  prerequisitesText: string | null;
  corequisitesText: string | null;
  outlineUrl: string | null;
}

