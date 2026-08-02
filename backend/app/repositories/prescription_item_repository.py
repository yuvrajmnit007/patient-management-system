from sqlalchemy.orm import Session

from app.models.prescription_item import PrescriptionItem


class PrescriptionItemRepository:

    @staticmethod
    def create_items(
        database: Session,
        items: list[PrescriptionItem],
    ):
        database.add_all(items)
        database.commit()

        for item in items:
            database.refresh(item)

        return items

    @staticmethod
    def get_items_by_prescription(
        database: Session,
        prescription_id: int,
    ):
        return (
            database.query(PrescriptionItem)
            .filter(
                PrescriptionItem.prescription_id == prescription_id
            )
            .all()
        )

    @staticmethod
    def delete_items(
        database: Session,
        prescription_id: int,
    ):
        (
            database.query(PrescriptionItem)
            .filter(
                PrescriptionItem.prescription_id == prescription_id
            )
            .delete()
        )

        database.commit()

    @staticmethod
    def update_items(
        database: Session,
        prescription_id: int,
        items: list[PrescriptionItem],
    ):
        (
            database.query(PrescriptionItem)
            .filter(
                PrescriptionItem.prescription_id == prescription_id
            )
            .delete()
        )

        database.add_all(items)
        database.commit()

        for item in items:
            database.refresh(item)

        return items