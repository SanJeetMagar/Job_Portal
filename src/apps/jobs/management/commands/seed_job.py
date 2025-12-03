from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import date

from src.apps.accounts.models import Company
from src.apps.jobs.models import Job


class Command(BaseCommand):
    help = "Seed a sample job post (TechCorp Senior React Developer)"

    def handle(self, *args, **options):
        User = get_user_model()

        # Ensure company user exists
        username = "techcorp"
        user, created = User.objects.get_or_create(username=username, defaults={
            "email": "contact@techcorp.com",
            "user_type": "company",
        })
        if created:
            user.set_password("password")
            user.save()
            self.stdout.write(self.style.SUCCESS(f"Created user '{username}' (password='password')"))
        else:
            self.stdout.write(f"User '{username}' already exists")

        company, c_created = Company.objects.get_or_create(
            company_name="TechCorp Inc.",
            defaults={
                "user": user,
                "description": "Leading technology company specializing in enterprise solutions",
                "website": "https://techcorp.com",
            },
        )
        if c_created:
            self.stdout.write(self.style.SUCCESS("Created Company 'TechCorp Inc.'"))
        else:
            # ensure the company is linked to the user
            if company.user_id != user.id:
                company.user = user
                company.save()
            self.stdout.write("Company 'TechCorp Inc.' already exists")

        # Sample job data
        job_data = {
            "title": "Senior React Developer",
            "description": "We're looking for an experienced React developer to join our team building innovative web applications. You'll be working on cutting-edge projects using the latest technologies and frameworks.",
            "salary": "$120,000 - $150,000",
            "location": "San Francisco, CA",
            "job_type": "Full-time",
            "posted": date.fromisoformat("2025-11-29"),
            "requirements": [
                "5+ years of React experience",
                "Strong TypeScript knowledge",
                "Experience with Next.js",
                "Familiar with modern testing frameworks",
                "Understanding of RESTful APIs",
                "Knowledge of modern build tools",
            ],
            "responsibilities": [
                "Develop new user-facing features",
                "Build reusable components",
                "Translate designs into code",
                "Optimize for performance",
                "Collaborate with product team",
            ],
            "benefits": [
                "Health insurance",
                "Remote work options",
                "Stock options",
                "Learning budget",
                "Flexible hours",
            ],
            "company_info": {
                "name": "TechCorp Inc.",
                "industry": "Technology",
                "size": "500-1000 employees",
                "website": "https://techcorp.com",
                "about": "Leading technology company specializing in enterprise solutions",
                "rating": 4.5,
                "reviews": 128,
                "founded": "2010",
                "headquarters": "San Francisco, CA",
            },
            "applicants_count": 42,
            "saved": False,
            "urgent": True,
            "application_deadline": date.fromisoformat("2025-12-31"),
            "remote_policy": "Hybrid (3 days in office)",
            "experience_level": "Senior",
            "education": "Bachelor's Degree",
        }

        job, j_created = Job.objects.get_or_create(
            company=company,
            title=job_data["title"],
            defaults={
                "description": job_data["description"],
                "salary": job_data["salary"],
                "location": job_data["location"],
                "job_type": job_data["job_type"],
                "posted": job_data["posted"],
                "requirements": job_data["requirements"],
                "responsibilities": job_data["responsibilities"],
                "benefits": job_data["benefits"],
                "company_info": job_data["company_info"],
                "applicants_count": job_data["applicants_count"],
                "saved": job_data["saved"],
                "urgent": job_data["urgent"],
                "application_deadline": job_data["application_deadline"],
                "remote_policy": job_data["remote_policy"],
                "experience_level": job_data["experience_level"],
                "education": job_data["education"],
            },
        )

        if j_created:
            self.stdout.write(self.style.SUCCESS(f"Created job '{job.title}' (id={job.id})"))
        else:
            # update in case some fields changed
            Job.objects.filter(id=job.id).update(
                description=job_data["description"],
                salary=job_data["salary"],
                location=job_data["location"],
                job_type=job_data["job_type"],
                posted=job_data["posted"],
                requirements=job_data["requirements"],
                responsibilities=job_data["responsibilities"],
                benefits=job_data["benefits"],
                company_info=job_data["company_info"],
                applicants_count=job_data["applicants_count"],
                saved=job_data["saved"],
                urgent=job_data["urgent"],
                application_deadline=job_data["application_deadline"],
                remote_policy=job_data["remote_policy"],
                experience_level=job_data["experience_level"],
                education=job_data["education"],
            )
            self.stdout.write(self.style.SUCCESS(f"Updated existing job '{job.title}' (id={job.id})"))

        self.stdout.write(self.style.NOTICE("Seeding complete. Use the API endpoints to fetch job details."))
